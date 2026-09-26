/**
 * Applying AI at Work native course doc sync.
 * Adapted from profsathya/Common-Curriculum apps-script/CourseDocSync.gs.
 *
 * Receives one course's context payload from GitHub Actions and rewrites the
 * named tabs of that course's Google Doc. The Course 180 document has Course,
 * Dojo, and Dojo Labs tabs; a payload names only the tabs to update, and every
 * other tab is left completely alone.
 *
 * This receiver does not create tabs. Add them once in Google Docs, then keep
 * their titles matching the section names sent by the sync client.
 *
 * The doc is downstream of the repo. Any edit made in a synced tab is lost the
 * next time that tab syncs.
 *
 * Script properties this expects:
 *   COURSE_DOC_SYNC_TOKEN  shared secret, must match the GitHub secret
 *   COURSE_DOC_IDS         JSON map, e.g. {"cst499":"1AbC...","cst286":"1XyZ..."}
 */

var TOKEN_PROPERTY = "COURSE_DOC_SYNC_TOKEN";
var DOC_MAP_PROPERTY = "COURSE_DOC_IDS";

function doPost(e) {
  var parsed = parsePayload(e);
  if (!parsed.ok) {
    return jsonResponse({ ok: false, error: parsed.error, message: parsed.message });
  }

  var payload = parsed.payload;
  var props = PropertiesService.getScriptProperties();
  var expectedToken = props.getProperty(TOKEN_PROPERTY);

  if (!expectedToken) {
    return jsonResponse({
      ok: false,
      error: "missing_token_property",
      message: "Script property " + TOKEN_PROPERTY + " is not set."
    });
  }
  if (!payload.token || payload.token !== expectedToken) {
    return jsonResponse({ ok: false, error: "invalid_token", message: "Missing or invalid sync token." });
  }
  if (!payload.course) {
    return jsonResponse({ ok: false, error: "missing_course", message: "Payload must name a course." });
  }
  if (!Array.isArray(payload.sections) || payload.sections.length === 0) {
    return jsonResponse({
      ok: false,
      error: "invalid_payload",
      message: "Payload must include a non-empty sections array."
    });
  }

  var docId = lookupDocId(props, payload.course);
  if (!docId) {
    return jsonResponse({
      ok: false,
      error: "unknown_course",
      message: "No document ID for course '" + payload.course + "' in " + DOC_MAP_PROPERTY + "."
    });
  }

  if (payload.document_id !== docId) {
    return jsonResponse({ok: false, error: "document_id_mismatch"});
  }

  var lock = LockService.getScriptLock();
  if (!lock.tryLock(30000)) {
    return jsonResponse({ ok: false, error: "lock_timeout", message: "Could not acquire the sync lock." });
  }

  try {
    var versions = checkVersions(props, docId, payload);
    var written = rebuildDocument(docId, payload);
    Object.keys(versions).forEach(function(tab) {
      versions[tab].rendered_digest = written.digests[tab];
      props.setProperty(versionKey(docId, tab), JSON.stringify(versions[tab]));
    });
    return jsonResponse({
      ok: true,
      course: payload.course,
      document_id: docId,
      tabs_written: written.tabs,
      versions: versions,
      page_count: written.pages,
      updated_at: new Date().toISOString()
    });
  } catch (err) {
    return jsonResponse({ ok: false, error: "document_update_failed", message: String(err) });
  } finally {
    lock.releaseLock();
  }
}

function versionKey(docId, tab) { return "VERSION:" + docId + ":" + tab; }

// The single native workflow uses monotonic GitHub run IDs and checks out current main
// after acquiring job serialization. Reruns retain their original generation.
function checkVersions(props, docId, payload) {
  var metadata = payload.metadata || {};
  if (!Number.isSafeInteger(metadata.generation) || metadata.generation < 1 || !metadata.repository || !metadata.commit_sha) {
    throw new Error("missing_source_generation");
  }
  var versions = {};
  payload.sections.forEach(function(section) {
    if (!section.tab || versions[section.tab] || !Array.isArray(section.pages) ||
        !/^[a-f0-9]{64}$/.test(section.content_digest || "") ||
        !/^[a-f0-9]{64}$/.test(section.rendered_digest || "")) {
      throw new Error("invalid_section");
    }
    var old = JSON.parse(props.getProperty(versionKey(docId, section.tab)) || "null");
    if (old && (old.repository !== metadata.repository || old.generation > metadata.generation ||
        (old.generation === metadata.generation && old.content_digest !== section.content_digest))) {
      throw new Error("stale_or_conflicting_generation");
    }
    versions[section.tab] = {generation: metadata.generation, repository: metadata.repository,
      commit_sha: metadata.commit_sha, content_digest: section.content_digest, release_id: section.release_id || null};
  });
  return versions;
}

function lookupDocId(props, course) {
  var raw = props.getProperty(DOC_MAP_PROPERTY);
  if (!raw) {
    return null;
  }
  try {
    var map = JSON.parse(raw);
    return map[course] || null;
  } catch (err) {
    return null;
  }
}

function parsePayload(e) {
  if (!e || !e.postData || !e.postData.contents) {
    return { ok: false, error: "missing_body", message: "Request must include a JSON body." };
  }
  try {
    return { ok: true, payload: JSON.parse(e.postData.contents) };
  } catch (err) {
    return { ok: false, error: "invalid_json", message: String(err) };
  }
}

/**
 * Collect the document's tabs by title, including nested ones, so a tab that
 * gets dragged under another still resolves.
 */
function collectTabs(tabs, found) {
  for (var i = 0; i < tabs.length; i++) {
    var tab = tabs[i];
    found[tab.getTitle()] = tab;
    var children = tab.getChildTabs();
    if (children && children.length) {
      collectTabs(children, found);
    }
  }
  return found;
}

function rebuildDocument(docId, payload) {
  var doc = DocumentApp.openById(docId);
  var tabsByTitle = collectTabs(doc.getTabs(), {});

  // Resolve every tab before writing anything, so one bad title can't leave
  // the document half-updated.
  var targets = [];
  for (var i = 0; i < payload.sections.length; i++) {
    var section = payload.sections[i];
    var tab = tabsByTitle[section.tab];
    if (!tab) {
      var available = Object.keys(tabsByTitle).join(", ") || "none";
      throw new Error(
        "This document has no tab titled '" + section.tab + "'. Tabs found: " + available +
        ". Add the tab in Google Docs, or fix the title in config/course-docs.json."
      );
    }
    targets.push({ section: section, tab: tab });
  }

  // A prior request may have saved the document but lost its receipt. Verify
  // the actual text before rewriting a large tab on a same-generation retry.
  var existingDigests = {};
  var alreadyCurrent = targets.every(function(target) {
    var digest = bodyDigest(target.tab.asDocumentTab().getBody());
    existingDigests[target.section.tab] = digest;
    return digest === target.section.rendered_digest;
  });
  if (alreadyCurrent) {
    return { tabs: [], pages: targets.reduce(function(total, target) {
      return total + target.section.pages.length;
    }, 0), digests: existingDigests };
  }

  // Preserve existing tab bodies for recovery if rendering or saving fails.
  var backups = targets.map(function(target) { return target.tab.asDocumentTab().getBody().copy(); });
  try {
  var titles = [];
  var pages = 0;
  for (var j = 0; j < targets.length; j++) {
    writeSection(targets[j].tab.asDocumentTab().getBody(), targets[j].section, payload);
    titles.push(targets[j].section.tab);
    pages += (targets[j].section.pages || []).length;
  }

  doc.saveAndClose();
  var readback = DocumentApp.openById(docId);
  var readTabs = collectTabs(readback.getTabs(), {});
  var digests = {};
  payload.sections.forEach(function(section) {
    var digest = bodyDigest(readTabs[section.tab].asDocumentTab().getBody());
    if (digest !== section.rendered_digest) { throw new Error("document_readback_mismatch"); }
    digests[section.tab] = digest;
  });
  return { tabs: titles, pages: pages, digests: digests };
  } catch (error) {
    doc = DocumentApp.openById(docId);
    var restoreTabs = collectTabs(doc.getTabs(), {});
    targets.forEach(function(target, index) {
      var body = restoreTabs[target.section.tab].asDocumentTab().getBody();
      body.clear();
      var backup = backups[index];
      for (var k = 0; k < backup.getNumChildren(); k++) {
        var child = backup.getChild(k).copy();
        switch (child.getType()) {
          case DocumentApp.ElementType.PARAGRAPH: body.appendParagraph(child.asParagraph()); break;
          case DocumentApp.ElementType.LIST_ITEM: body.appendListItem(child.asListItem()); break;
          case DocumentApp.ElementType.TABLE: body.appendTable(child.asTable()); break;
          default: throw new Error("Unsupported backup element; inspect document recovery: " + child.getType());
        }
      }
    });
    doc.saveAndClose();
    throw error;
  }
}

function bodyDigest(body) {
  var text = body.getText().split(/\r?\n/)
    .map(function(line) { return line.trim(); }).filter(function(line) { return line.length > 0; }).join("\n");
  return Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256, text, Utilities.Charset.UTF_8)
    .map(function(byte) { return (byte < 0 ? byte + 256 : byte).toString(16).padStart(2, "0"); }).join("");
}

function writeSection(body, section, payload) {
  body.clear();

  body.appendParagraph(section.heading || payload.title || payload.course)
    .setHeading(DocumentApp.ParagraphHeading.HEADING1);

  if (section.intro) {
    body.appendParagraph(section.intro).editAsText().setItalic(true);
  }

  body.appendParagraph("Last updated " + (payload.generated_at_pacific || "unknown") + ".")
    .editAsText().setItalic(true).setFontSize(9);
  body.appendParagraph("Source version: " + (section.release_id || section.content_digest) +
    " | Generation: " + payload.metadata.generation).editAsText().setFontSize(9);
  body.appendParagraph("");

  (section.pages || []).forEach(function (page) {
    body.appendParagraph(page.title || page.path)
      .setHeading(DocumentApp.ParagraphHeading.HEADING1);
    renderContent(body, page.content || "");
    body.appendParagraph("");
  });

  if (Array.isArray(section.glossary) && section.glossary.length > 0) {
    body.appendParagraph("Glossary")
      .setHeading(DocumentApp.ParagraphHeading.HEADING1);
    section.glossary.forEach(function (entry) {
      body.appendParagraph(entry.term)
        .setHeading(DocumentApp.ParagraphHeading.HEADING3);
      body.appendParagraph(entry.definition || "");
    });
  }
}

function renderContent(body, content) {
  String(content).split(/\r?\n/).forEach(function (line) {
    if (line.trim() === "") {
      return;
    }

    var heading = line.match(/^(#{1,6})\s+(.+)$/);
    if (heading) {
      body.appendParagraph(heading[2].trim()).setHeading(headingFor(heading[1].length));
      return;
    }

    if (line.indexOf("- ") === 0) {
      body.appendListItem(line.substring(2)).setGlyphType(DocumentApp.GlyphType.BULLET);
      return;
    }

    var bold = line.match(/^\*\*(.+)\*\*$/);
    if (bold) {
      body.appendParagraph(bold[1]).editAsText().setBold(true);
      return;
    }

    body.appendParagraph(line);
  });
}

function headingFor(level) {
  if (level <= 1) {
    return DocumentApp.ParagraphHeading.HEADING2;
  }
  if (level === 2) {
    return DocumentApp.ParagraphHeading.HEADING2;
  }
  if (level === 3) {
    return DocumentApp.ParagraphHeading.HEADING3;
  }
  return DocumentApp.ParagraphHeading.HEADING4;
}

function jsonResponse(payload) {
  return ContentService
    .createTextOutput(JSON.stringify(payload))
    .setMimeType(ContentService.MimeType.JSON);
}
