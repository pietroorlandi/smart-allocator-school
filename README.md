# Resource Allocator for Connecting Unconnected Schools

<img src="image/logo.png" alt="Project Logo" width="250" />

## Project Overview
This project provides a solution to optimize the allocation of funds for connecting unconnected schools, focusing on areas with limited or no internet access. By analyzing input data such as school locations, population density, available technologies, and budget constraints, the system generates actionable recommendations to maximize impact.

## Key Features
- Prioritizes schools based on geographic and demographic factors.
- Recommends the most suitable connectivity technology for each school.
- Ensures efficient resource allocation within budget limits.
- Outputs a clear, detailed report with actionable insights.

## Getting Started
### Prerequisites
- Python 3.11
- Required libraries (see `requirements.txt`)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/pietroorlandi/smart-allocator-school.git
   cd smart-allocator-school
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Usage
1. Prepare input data (schools, budget, and available technologies) in the required format.
2. Run the system:
   ```bash
   streamlit run src/gui/app.py
   ```
4. Insert the API key for the LLM in the GUI and run the application
3. Review the generated output for recommendations.

## Demo Video
Check out a quick demo of the project in action:

[![See the demo](https://img.youtube.com/vi/UyJ5z9j-nJE/0.jpg)](https://www.youtube.com/watch?v=UyJ5z9j-nJE&ab_channel=PietroAnonimo)


## Contributing
Contributions are welcome! To contribute:
1. Fork this repository.
2. Create a new feature branch.
3. Commit your changes.
4. Submit a pull request for review.


## Acknowledgments
Thanks to all contributors and stakeholders for their support and feedback.
