# .CBZ ComicInfo.xml summary formatter for Jellyfin

This python script loops through all your .cbz files in the same directory and reformats all ComicTagger summaries to <![CDATA[]]> HTML encoded data so that jellyfin can render it properly on your web browser and in your Jellyfin app on mobile devices. 

Only .cbz files are supported.

It will open and extract the file structure of your .cbz files, look for a ComicInfo.xml and open it, then it reads the `<Summary>` tag, wraps the content in a `<![CDATA[]]>` tag and reformats all `\n` (newlines) to `<br />` tags and save the file.
