# GPS Toll-Based System

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Setup and Installation](#setup-and-installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)
- [Contact](#contact)

## Introduction
The **GPS Toll-Based System** is a comprehensive solution for managing toll collection using GPS technology. This system tracks vehicles' journeys, calculates toll charges, provides invoices, and issues penalties for unpaid tolls. The project includes a front-end developed with HTML, CSS, and JavaScript, and a back-end powered by Django and SQLite. 

## Features
- Real-time vehicle tracking using GPS
- Automated toll calculation based on vehicle journey
- Toll invoices generation
- Google Authentication for secure access
- Penalty and warning system for unpaid tolls

## Technologies Used
- **Front-end**: HTML, CSS, JavaScript
- **Back-end**: Django, SQLite
- **Libraries**: NumPy, Zendpanda, Geopanda, SleepleteJS
- **Hardware**: Arduino, GSM800 module

## Setup and Installation
To run this project locally, follow these steps:

1. **Clone the repository**
    ```bash
    git clone https://github.com/MAYANK12SHARMA/GPS-Toll-Checker.git
    ```

2. **Navigate to the project directory**
    ```bash
    cd GPS_Toll_Tax
    ```

3. **Install the required dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Apply database migrations**
    ```bash
    python manage.py migrate
    ```

5. **Run the development server**
    ```bash
    python manage.py runserver
    ```

## Usage
1. Access the application at `http://localhost:8000`.
2. Register or log in using Google Authentication.
3. Connect the Arduino and GSM800 module to start tracking.
4. View toll charges, invoices, and penalty warnings on your dashboard.


## Screenshots

### Sign up page

![image](https://github.com/MAYANK12SHARMA/GPS-Toll-Checker/assets/145884197/52689bdb-19af-4674-95bf-65f9d441a839)

### Login Page

![image](https://github.com/MAYANK12SHARMA/GPS-Toll-Checker/assets/145884197/29ddb425-b6dc-4d1f-a044-5cd4f1e1eeb5)

### Dashboard

![Dashboard](https://github.com/MAYANK12SHARMA/GPS-Toll-Checker/assets/145884197/4be7f900-52d3-468e-9b0d-68e34e06fc42)

![image](https://github.com/MAYANK12SHARMA/GPS-Toll-Checker/assets/145884197/60185960-af0d-43b7-bbdb-f6e79910eeef)

### Add vehicle Section

![image](https://github.com/MAYANK12SHARMA/GPS-Toll-Checker/assets/145884197/d694f703-a303-48a0-9875-798cc828f916)

### Vehicle Details 

![image](https://github.com/MAYANK12SHARMA/GPS-Toll-Checker/assets/145884197/989b2036-1b6b-448f-9645-76cad7634a3c)

### Journey Section

![image](https://github.com/MAYANK12SHARMA/GPS-Toll-Checker/assets/145884197/30508dce-cd61-4eff-90a2-0bdfbdfb7359)

#### Example 
![image](https://github.com/MAYANK12SHARMA/GPS-Toll-Checker/assets/145884197/e5c927ea-51e1-4bb1-9274-3ba1019dc50c)

![image](https://github.com/MAYANK12SHARMA/GPS-Toll-Checker/assets/145884197/ea6c56fa-e594-433f-aa3e-5799cb7b401b)

### Invoice Page After Journey

![image](https://github.com/MAYANK12SHARMA/GPS-Toll-Checker/assets/145884197/5c51388a-d890-4ecd-a571-9628ed562337)


### Billing Section 

![image](https://github.com/MAYANK12SHARMA/GPS-Toll-Checker/assets/145884197/281cb9cf-9ab1-4a59-83e1-480d6f16cf1f)

### Enquiry Section

![image](https://github.com/MAYANK12SHARMA/GPS-Toll-Checker/assets/145884197/b9f9a2f9-d4e2-411f-b20d-0424695d4eb2)



## Contributing
Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements
- **Intel Unity Program** for project support
- **GLA University** for mentorship and resources


## Contact
- **Mayank Sharma**
  - Email: [mayank.sharma_cs.h23@gla.ac.in](mailto:mayank.sharma_cs.h23@gla.ac.in)



