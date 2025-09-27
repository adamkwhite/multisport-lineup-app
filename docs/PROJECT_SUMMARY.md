# Baseball Lineup Management Application - Project Summary

## **What You Asked For:**
A web application that integrates with TeamSnap API to automatically generate baseball fielding lineups for personal use, specifically designed for youth baseball games.

## **Core Requirements:**
1. **TeamSnap Integration** - Connect to TeamSnap API, authenticate with OAuth, and fetch team data
2. **Game Management** - Retrieve upcoming games and player availability 
3. **Lineup Generation** - Create baseball fielding positions automatically
4. **Print-Friendly Output** - Generate lineups that can be printed and taken to the field

## **Key Challenge - 6-Inning Game Format:**
You specifically requested: *"We play 6 innings, we can only have a pitcher pitch for 2 innings per game. Can you generate 3 possible lineups for each game, that don't repeat pitchers. I'd like to print them and take them to the field."*

---

## **What I Built:**

### **1. Complete Flask Web Application**
- **Backend**: Python Flask with TeamSnap OAuth 2.0 integration
- **Frontend**: HTML/CSS/JavaScript with tabbed interface
- **Database**: SQLAlchemy models for data management
- **Security**: HTTPS setup with SSL certificates for local development

### **2. TeamSnap API Integration**
- OAuth authentication flow
- Team filtering (All, Active, Archived, with "Cobs" as default)
- Game retrieval with filtering (Next Game Only vs All Upcoming Games)
- Player availability checking (only confirmed attending players)
- Automatic exclusion of coaches/managers from player lineups

### **3. Position Preference System**
- **Any Position**: Default preference, players randomized across different positions in the 3 lineups
- **Pitcher**: Designated pitchers rotated across lineups (no pitcher repeats)
- **Catcher**: Designated catchers rotated across lineups if multiple available

### **4. Smart Lineup Generation**
- **3 Complete Lineups** for 6-inning games:
  - Lineup 1: Innings 1-2
  - Lineup 2: Innings 3-4  
  - Lineup 3: Innings 5-6
- **Pitcher Rotation**: Ensures no pitcher plays more than 2 innings
- **Catcher Rotation**: Rotates multiple catchers across lineups
- **Position Variety**: Randomizes "any position" players so they don't play the same position all game

### **5. Visual Baseball Diamond Display**
- Interactive baseball field graphics with proper positioning
- Position cards showing player names and position numbers (1-9)
- Realistic field layout with bases, pitcher's mound, and home plate
- Adjustable sizing (currently 700px × 600px)

### **6. Print-Optimized Design**
- **Clean Print Layout**: Removes navigation, headers, and buttons when printing
- **Page Breaks**: Each lineup on separate page for easy field reference
- **Essential Info Only**: Shows "3 Lineups • 2 Innings Each • No Repeated Pitchers"
- **Field Graphics**: All 3 lineups display as baseball diamonds (not lists)

### **7. User Interface Features**
- **Tabbed Navigation**: Select Team & Game → Players → Lineup
- **Team Filtering**: Filter by team status with smart defaults
- **Game Selection**: Choose specific games from upcoming schedule
- **Player Management**: View attending players with position preferences
- **Easy Navigation**: "Back to Players" button, regenerate lineup option

---

## **Technical Achievements:**
- Solved TeamSnap API authentication and HTTPS requirements
- Fixed multiple API integration issues (field names, timezone handling)
- Created responsive, print-friendly design
- Implemented complex rotation logic for pitchers and catchers
- Built visual baseball field representation
- Added randomization for position variety

## **Key Files:**
- `app.py` - Main Flask application with TeamSnap API integration and lineup generation logic
- `templates/dashboard.html` - Frontend interface with tabbed design and baseball field graphics
- `requirements.txt` - Python dependencies
- `README.md` - Setup and usage instructions
- `.env` - Environment configuration (TeamSnap API credentials)
- `PROJECT_SUMMARY.md` - Complete project overview and technical achievements
- `HOSTING_GUIDE.md` - Deployment options and hosting recommendations
- Todo list - Multi-user conversion and payment integration roadmap

## **Final Result:**
The application successfully addresses your core need: **generating 3 strategically different lineups for 6-inning games that can be printed and taken to the field, with proper pitcher rotation and position variety for player development.**

The system respects baseball rules (pitcher innings limits), promotes player development (position variety), and provides a practical tool for game management (print-friendly format).