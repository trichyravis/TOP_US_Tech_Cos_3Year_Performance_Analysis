# Assets Directory

This directory is reserved for:
- Logo images
- Icons
- Branding materials
- Static images for the app

## Usage

Place any image files (PNG, JPG, SVG) here that you want to use in the Streamlit app.

Example: To use a logo in the app, save it here as `logo.png` and reference it in the code:
```python
st.image('assets/logo.png', width=200)
```

## File Structure

```
assets/
├── .gitkeep              (keeps folder tracked in git)
└── [Your image files]
```

## Recommended Files to Add

- logo.png (300x300px) - Mountain Path logo
- favicon.ico - Browser tab icon
- mountain_background.png - Optional background image

**Note:** .gitkeep is a placeholder. Once you add actual files, you can delete it.
