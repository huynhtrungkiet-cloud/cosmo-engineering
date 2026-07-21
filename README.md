# Cosmo Engineering Marketplace

Marketplace cá nhân chứa plugin **cosmo-engineering** (3 skill kỹ thuật cơ khí).

## Cài vào Claude (claude.ai / app)

1. Đẩy repo này lên GitHub (xem bên dưới).
2. Trong Claude: **Settings** → bật **Code execution and file creation**.
3. Mở **Customize** (sidebar) → tab **Plugins** → mục **Personal plugins** → bấm **"+"** → **Add marketplace**.
4. Nhập repo GitHub của bạn (dạng `owner/cosmo-engineering-plugin`) hoặc URL `https://github.com/owner/cosmo-engineering-plugin`.
5. Sau khi marketplace hiện ra, **Install** plugin `cosmo-engineering`.

## Đẩy lên GitHub

```bash
cd cosmo-engineering-plugin
git init
git add .
git commit -m "Cosmo Engineering plugin v1.0.0"
git branch -M main
# tạo repo trống trên GitHub trước, rồi:
git remote add origin https://github.com/<owner>/cosmo-engineering-plugin.git
git push -u origin main
```

## Cấu trúc

```
cosmo-engineering-plugin/
├── .claude-plugin/
│   └── marketplace.json                # catalog marketplace (gốc repo)
└── plugins/
    └── cosmo-engineering/
        ├── .claude-plugin/
        │   └── plugin.json             # manifest plugin
        ├── skills/
        │   ├── machining-quotation/
        │   ├── coupling-dhp-advisory/
        │   └── mechanical-project-concept/
        └── README.md
```
