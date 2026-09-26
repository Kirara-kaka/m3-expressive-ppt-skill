# Material 3 Expressive Theming & Palette Reference

## Tonal Palette Derivation

Google Material 3 Expressive (`SchemeExpressive`) uses the HCT (Hue, Chroma, Tone) perceptual color space:
- **Hue**: Color wavelength (0-360).
- **Chroma**: Color intensity / colorfulness (0-120+). Expressive scheme drives chroma to high vibrancy levels.
- **Tone**: Perceptual lightness (0 = pure black, 100 = pure white).

### Dual-Chroma High-Contrast Dynamic Principle
Instead of a monochromatic palette, `SchemeExpressive` rotates the hue of the Tertiary palette by approximately 60-120 degrees relative to Primary, while maintaining complementary chromatic intensity.
- **Primary**: Brand anchor (Tone 40 in Light mode, Tone 80 in Dark mode).
- **Tertiary**: Punchy accent (Warm peach, lime mint, or bright amber) used on badges, chips, and key milestone cards.
- **Canvas / Background**: `surface_container_low` (Tone 96 in Light mode, Tone 10 in Dark mode). Eliminates plain `#FFFFFF` sterility and provides soft ambient tinting.

## Built-In Curated Presets

1. **`indigo_coral`** (Default Flagship)
   - Seed: `#3F51B5`
   - Primary: `#385EA4` (Deep Indigo)
   - Tertiary: `#006C50` (Vibrant Mint) / Coral Peach
   - Canvas: `#F1F3FF`
   - Vibe: Authoritative, enterprise-grade, high polish keynote.

2. **`electric_mint`** (Future Tech & Cloud)
   - Seed: `#00897B`
   - Primary: `#006A60` (Electric Teal)
   - Tertiary: `#8F4C38` (Warm Terracotta / Peach)
   - Canvas: `#E6F7F0`
   - Vibe: Fresh, agile, developer platforms, AI infrastructure.

3. **`digital_lavender`** (AI Native & Next-Gen)
   - Seed: `#7C4DFF`
   - Primary: `#5C53A5` (Digital Lavender)
   - Tertiary: `#006C4C` (Emerald Mint)
   - Canvas: `#F5F0FF`
   - Vibe: Creative, AI agents, avant-garde design systems.

4. **`warm_amber`** (Vibrant Leadership & Commerce)
   - Seed: `#FF6D00`
   - Primary: `#8B5000` (Warm Amber)
   - Tertiary: `#006495` (Sky Blue)
   - Canvas: `#FFF5EB`
   - Vibe: Energetic, product launch, consumer tech.
