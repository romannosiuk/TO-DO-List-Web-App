# TO-DO List Web Application

A modern, user-friendly web application for managing your tasks and to-do items. Built with Flask, featuring user authentication, task prioritization, and a beautiful UI.

Live: https://to-do-list-qc4p.onrender.com/register

## Features

- 🔐 **User Authentication** - Secure registration and login system
- ✅ **Task Management** - Create, edit, delete, and mark tasks as complete
- ⭐ **Priority System** - Mark important tasks with a star
- 📱 **Responsive Design** - Works on desktop and mobile devices
- 🎨 **Custom Styling** - Beautiful UI with custom fonts and colors
- 💾 **Persistent Storage** - SQLite database to save your tasks

## Tech Stack

- **Backend**: Flask 3.0.0
- **Database**: SQLAlchemy with SQLite
- **Frontend**: HTML5, CSS3, Bootstrap 5
- **Authentication**: Flask-Login
- **Forms**: Flask-WTF
- **Server**: Gunicorn (production)

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd "TO-DO List"
```

2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python main.py
```

5. Open your browser and visit: `http://localhost:5000`

## Demo Account

For quick testing, use the demo account:

- **Email**: `test@gmail.com`
- **Password**: `test`

This account is automatically created on first run with sample tasks to demonstrate all features.

## Usage

### Getting Started

1. **Register** - Create a new account with your email and password
2. **Login** - Sign in with your credentials
3. **Add Tasks** - Type a task and click "Create" to add it
4. **Manage Tasks**:
   - ⭐ Click the star to mark as high priority
   - ✓ Check the box to mark as complete
   - ✏️ Click "Edit" to modify the task
   - 🗑️ Click "Delete" to remove the task

### Task Features

- **Priority**: Toggle between normal and high priority tasks
- **Completion**: Mark tasks as done with checkboxes
- **Sorting**: Tasks are automatically sorted by priority and completion status
- **Auto-save**: All changes are saved immediately

## Project Structure

```
TO-DO List/
├── main.py                 # Main Flask application
├── forms.py               # WTForms form definitions
├── requirements.txt       # Python dependencies
├── Procfile              # Render deployment config
├── README.md             # This file
└── app/
    ├── templates/        # HTML templates
    │   ├── base.html
    │   ├── index.html
    │   ├── login.html
    │   ├── register.html
    │   └── edit_task.html
    └── static/           # Static files
        ├── style.css     # Custom styles
        └── fonts/        # Custom fonts
```

## Database

The application uses SQLite for data persistence. The database is automatically created on first run and stored in `instance/data.db`.

### Models

- **User** - Stores user account information
- **Task** - Stores task details linked to users

## Deployment

### Deploy to Render

1. Push your code to GitHub
2. Visit [render.com](https://render.com) and create a new Web Service
3. Connect your GitHub repository
4. Set the following:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn main:app`
5. Add environment variables:
   - `SECRET_KEY` - Your Flask secret key for security
6. Deploy!

### Environment Variables

For production deployment, set these environment variables:

- `SECRET_KEY` - Secret key for CSRF protection and sessions (required for production)
- `FLASK_ENV` - Set to `production` for production deployments

## Customization

### Colors and Styling

Edit `app/static/style.css` to customize:
- Background colors
- Button colors
- Font styles
- Checkbox appearance

### Fonts

Custom fonts are stored in `app/static/fonts/`. Add new fonts and update the CSS `@font-face` rules.

## Security

- ✅ Password hashing with PBKDF2-SHA256
- ✅ CSRF protection on all forms
- ✅ User authentication required for task management
- ✅ SQL injection protection via SQLAlchemy ORM

## Known Limitations

- SQLite database is not ideal for production with multiple users
- Consider using PostgreSQL for production deployments
- Maximum task size: 200 characters for title

## Future Enhancements

- [ ] Task categories/tags
- [ ] Due dates and reminders
- [ ] Task sharing between users
- [ ] Dark mode
- [ ] Task analytics dashboard

## Troubleshooting

### Port already in use
```bash
# Change the port in main.py:
app.run(host='0.0.0.0', port=8000)
```

### Database errors
```bash
# Delete the database and recreate it:
rm -rf instance/
python main.py
```

### Import errors
```bash
# Reinstall dependencies:
pip install --upgrade -r requirements.txt
```

## License

This project is open source and available under the MIT License.

## Support

For issues or questions, please open an issue in the repository.

---

**Made by Roman Nosiuk**
