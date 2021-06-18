**PyEditorial**

A free, open-source Blog CMS based on the "Django" and "Editorial" HTML5 theme.

**Features**

  * "Blog" section to create and edit a blog + Blog Category
  * "Videocast" section to create and edit a videocast + Videocast Category
  * "Podcast" section to create and edit a podcast + podcast Category
  * "Skill" section to create and edit a skill
  * "CONSTANCE" Section to manage dynamic Django settings (Blog title, Social Networks links and ...)
  * Displays the list of Blog posts as paged in archive
  * Displays the list of Videocast as paged in archive
  * Displays the list of podcast as paged in archive
  * Used "Django Admin" to manage all models
  * Used "Editorial" theme by HTML5 UP
  * Used "Sqlite" to create DB
  * Used "CKEditor"
  * Translation ready
  * Auth system (login & logout and forget a password)
  * Front-end forms to create new object

**How to install and run (GNU/Linux and Mac)**

  * Install git,python3, pip3, virtualenv in your operating system
  * Create a development environment ready by using these commands
  
    git clone https://github.com/puneetgarg2601/Frolic		# clone the project

    cd Frolic		                                        # go to the project DIR

    pip install -r requirements.txt		                        # Install project requirements in .venv

    python manage.py makemigrations		                        # Create migrations files

    python manage.py migrate		                        # Create database tables

    python manage.py collectstatic		                        # Create statics files

    python manage.py runserver		                        # Run the project


  * Go to http://127.0.0.1:8000/ to use project
    