# Educational Support Dashboard

## Overview
The Educational Support Dashboard is an interactive tool designed to assist educational counselors in identifying and prioritizing support for students in need. Utilizing school performance data, the dashboard highlights students with low math grades but high potential for improvement. The application provides intuitive visualizations and interactive features to enable easy data analysis and informed decision-making.

## Dashboards
Two dashboards were developed for this use case:
- Final Dashboard: non-customizable dashboard, pre-defined factor weights according to their correlation with the final math score.
- Final Dashbord Personnalisable: user-customizable factor weights.



## Requirements
- Python 3.9
- Streamlit
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Jupyter Notebook

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/baanass/Interactive-Dashboard-for-Prioritizing-Support-for-Students-in-Need
    ```
2. Navigate to the project directory:
    ```bash
    cd Interactive-Dashboard-for-Prioritizing-Support-for-Students-in-Need
    ```
3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage
1. Execute the dashboard:
    ```bash
    streamlit run .\src\script\dashboard_final.py
    ```
    
2. Open the provided URL in your web browser to interact with the dashboard.

## Data Analysis
The data analysis was conducted using Jupyter Notebook and python scripts. The notebook used for data analysis is located in the `notebooks` directory. The python scripts contain the data cleaning, preprocessing, and analysis to plot the dashboards.


## Future Development
The project aims to expand with additional dashboards focusing on various aspects of educational data analysis. Each dashboard will be developed and executed independently to provide specific insights and support decision-making processes in different areas.

## Contributing
Contributions are welcome! If you have any ideas, suggestions, or improvements, please feel free to submit a pull request or open an issue.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contact
For any questions or further information, please contact:
- [Anass Baba](https://www.linkedin.com/in/baba-anass/)
- Email: baba.anass@outlook.com

