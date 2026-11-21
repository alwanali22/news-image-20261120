Fonts bundled with this entry (v4.4)

The five TrueType files in this folder are the DejaVu fonts
(DejaVuSerif-Bold, DejaVuSans-Bold, DejaVuSans,
DejaVuSansCondensed, DejaVuSansCondensed-Bold), copied unchanged
from the Debian fonts-dejavu / fonts-dejavu-extra packages.

DejaVu fonts are free software, freely redistributable: they are
based on Bitstream Vera (released under a permissive licence) with
additions in the public domain; see the DejaVu licence
(https://dejavu-fonts.github.io/ — "Fonts are (c) Bitstream, Inc.
and are released under the Bitstream Vera licence; additions are
public domain").

They are bundled so the entry renders identically on any machine,
including the grading server, which may not have the
fonts-dejavu-extra package (DejaVuSansCondensed) installed.
draw_v4.py loads them from this folder first and falls back to
/usr/share/fonts/truetype/dejavu if they are missing.
