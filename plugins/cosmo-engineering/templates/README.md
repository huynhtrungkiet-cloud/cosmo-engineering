# CE drawing template / Template bản vẽ CE

Put the exported template here as **`CE-TEMPLATE.dxf`** (DXF 2018 / AC1032).

Export once from AutoCAD Mechanical: open `TEMPLATE.dwg` → `SAVEAS` → type *AutoCAD 2018 DXF (*.dxf)*
→ name `CE-TEMPLATE.dxf`. The `.dwg` itself cannot be read by the Python toolchain (ezdxf reads DXF only).

Then verify the title-block attribute tags the script will fill:

```bash
python plugins/cosmo-engineering/skills/project-pipeline/scripts/fill_titleblock.py --list \
       --template plugins/cosmo-engineering/templates/CE-TEMPLATE.dxf
```

It prints every block that has attributes (`Title Blocks COSMO`, revision table, …) with each tag and
prompt (e.g. `Title`, `Part Number`, `Designed by 01`). Copy those tags into `templates/titleblock-map.json`
if they differ from the defaults in the script. See `skills/project-pipeline/references/ce-standards.md` §2.
