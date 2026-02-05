# 🗡️ TBC Leveling Logbook

**Your Complete Guide from Level 60 to 70**

A beautiful, interactive web application for tracking your World of Warcraft: The Burning Crusade leveling progress. Designed for 5-man groups looking to efficiently level from 60 to 70 while obtaining heroic keys and raid attunements.

![TBC Theme](tbc_logo.webp)

## ✨ Features

- **📋 Complete Task Checklist** - 159 carefully curated tasks including quests, dungeons, and grinding spots
- **💾 Progress Tracking** - Automatic save to browser localStorage - never lose your progress
- **🔍 Smart Filtering** - Filter by task type (Quests, Dungeons, Grind, Milestones, Other)
- **🔎 Search Functionality** - Quickly find specific tasks
- **🧮 XP Calculator** - Calculate experience needed between any two levels (60-70)
- **📊 Live Statistics** - Track completion percentage and estimated level
- **ℹ️ Information Panel** - General tips, requirements, and disclaimers
- **🎨 TBC Fel Green Theme** - Authentic Burning Crusade aesthetic with custom background

## 🚀 Live Demo

[**Visit the Live App**](#) *(URL will be added after Render deployment)*

## 📸 Screenshots

*Coming soon*

## 🛠️ Technology Stack

- **Pure HTML/CSS/JavaScript** - No frameworks, no dependencies
- **localStorage API** - Client-side progress persistence
- **Responsive Design** - Works on desktop and mobile
- **Modern CSS** - Glassmorphism effects, gradients, and animations

## 📦 Project Structure

```
tbc-leveling/
├── index_complete.html    # Main application file (self-contained)
├── fondo.avif            # Background image
├── tbc_logo.webp         # TBC logo
├── leveling_data.json    # Source data (tasks, XP table, info)
└── build_with_theme.py   # Build script to generate final HTML
```

## 🎯 Usage

1. Open `index_complete.html` in your browser
2. Click checkboxes to mark tasks as complete
3. Use filters to focus on specific task types
4. Search for specific quests or dungeons
5. Track your progress in the stats panel
6. Use the XP calculator to plan your leveling

## 🔧 Development

To rebuild the HTML file with updated data:

```bash
python build_with_theme.py
```

This will:
- Load data from `leveling_data.json`
- Embed it into the HTML template
- Apply the TBC green theme
- Generate `index_complete.html`

## 📝 Data Structure

The `leveling_data.json` file contains:

```json
{
  "introduction": {
    "general_info": ["..."],
    "xp_table": [...]
  },
  "route": [
    {
      "id": 4,
      "type": "quest",
      "name": "Task Name",
      "notes": "Additional information",
      "rewards": "XP/Items"
    }
  ]
}
```

## 🎨 Customization

### Colors

The app uses CSS custom properties for easy theming. Main colors:

- `--tbc-green: #00FF96` - Primary fel green
- `--tbc-green-dark: #00CC77` - Darker shade
- `--bg-dark: #0a0e0a` - Background

### Background

Replace `fondo.avif` with your own background image.

### Logo

Replace `tbc_logo.webp` with your own logo.

## 📄 License

This project is for educational and personal use. World of Warcraft and The Burning Crusade are trademarks of Blizzard Entertainment.

## 🙏 Credits

Data compiled from various online resources and content creators in the WoW Classic community.

## 🐛 Issues & Contributions

Found a bug or have a suggestion? Feel free to open an issue or submit a pull request!

---

**Made with ❤️ for the WoW Classic TBC community**
