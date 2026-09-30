# Local narrated videos

Artifact bodies use a fenced `video` block containing JSON with exactly `src`, `title`, and `captions`. Keep the MP4 and English WebVTT inside the artifact's adjacent `assets/` directory. For example:

```video
{"src":"assets/setup.mp4","title":"Set up your coach","captions":"assets/setup.vtt"}
```

The renderer creates a native video player with controls, inline playback, metadata preload, a descriptive accessible label, English captions enabled by default, and a visible download link. Schema validation rejects missing files, paths outside `assets/`, symlinks escaping it, unsupported formats, and malformed blocks. Publication copies the original assets into the existing Common Curriculum site with content-addressed names; changes to media or captions change the hosted page hash. Publish recovery snapshots include every media file.

The Dojo walkthroughs are the instructor's narrated September 29 originals. Their SHA-256 hashes are `8a957cc481979b6874f11e5b5824298553ca17c139f74619f4dfffd2654f5616` (ChatGPT) and `f1d429e5a7f0d6b754726d17785d809a01302f9ca86f3a3bd800ab80ae6687a7` (Gemini). English captions use the existing WhisperX word-aligned transcripts of the matching narration WAVs. No video or audio was re-encoded.
