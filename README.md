# Group 1 Project - SterLearning

Gamified learning tool about budget and finance for young people navigating their first job. In-game rewards and competition are used to motivate users. Users will earn an in-game currency which they can use to customize an avatar.

The final commit on `release` will be marked. It is up to the technical lead to decide when `trunk` should be merged into `release`, but at least 3 other team members should approve. 


### Quick Links

- [Group static site](https://csee.pages.surrey.ac.uk/com2027/2023-24/Group1)
- [Problem statement (SurreyLearn)](https://surreylearn.surrey.ac.uk/d2l/le/lessons/252863/topics/2968063)
- [PEP8 (styling guide)](https://peps.python.org/pep-0008/)


## Technologies Used

For our back-end, we will be using [Django](https://www.djangoproject.com/). The database used with Django is SQLite.

The front-end framework is [Bootstrap](https://getbootstrap.com/), including [Bootstrap icons](https://icons.getbootstrap.com/).

This GitLab repository should be the only used for the project.


## Project Structure

- */SterLearning/* - Django project configuration
- */app_admin/* - App for custom admin system
- */app_leaderboard/* - App for real-time leaderboard system
- */app_pages/* - App to contain all generic web pages
- */app_quiz/* - App for the quizzing system
- */app_tools/* - App for the finance tools
- */app_user/* - App for user management
- */locale/* - Folder for string localisation
- */templates/* - Folder to contain all site-wide HTML templates, e.g. header
- */static/* - Folder to contain all site-wide static content, e.g. avatars, JavaScript, CSS, etc.
- */com2027.yml* - YAML file used to configure the static site

*sub-apps may also contain a templates or static folder if they require one*


## Branching Instructions

This project uses feature centric branching so you will need to switch branches often. To ensure you push your code to the correct branch, you should ensure all previous code has been pushed to the GitLab repository and use the following commands in your local repository.
```
git fetch
git switch 2-create-skeleton-code
```
(To use the remote branch `2-create-skeleton-code`)


## Best Practices

When writing code for this project, you should always adhere to DRY (Don't Repeat Yourself) and follow the [PEP8](ttps://peps.python.org/pep-0008/) style guide. The style guide will be enforced by a linter (pylint) as part of the pipeline. *Spaces* should always be used in favour of *tab* for indentation, as outlined in the style guide. Python **does not** allow mixing of tabs and spaces for indentation. Your code should be well commented to make it easier for another team member to work with in the future.

When writing code, notes should be taken for use later in the writing of the FAR.