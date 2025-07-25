<a name="readme-top"></a>

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]



<br />
<div align="center">
<h3 align="center">CodeForHer Backend</h3>

  <p align="center">
    🏆 <strong>Winner - Locus CodeForHer Hackathon</strong><br />
    A platform dedicated to empowering women in technology through coding education and community support.
    <br />
    <a href="https://github.com/Ashishkumaraswamy/CodeForHer-Backend"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="YOUR_DEMO_LINK">View Demo</a>
    ·
    <a href="https://github.com/Ashishkumaraswamy/CodeForHer-Backend/issues">Report Bug</a>
    ·
    <a href="https://github.com/Ashishkumaraswamy/CodeForHer-Backend/issues">Request Feature</a>
    <br />
    <br />
    🔗 <a href="https://www.hindustantimes.com/genesis/safer-roads-by-code-india-s-next-gen-hack-transforming-safety-101750678135616.html">Know More About the Hackathon »</a>
  </p>
</div>




<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Screenshot][product-screenshot]](YOUR_DEMO_LINK)

CodeForHer is a platform designed to empower women in technology by providing accessible coding education, mentorship opportunities, and a supportive community. Our mission is to bridge the gender gap in tech by offering resources and support tailored to women's needs in the industry.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* [![Python][Python.com]][Python-url]
* [![FastAPI][FastAPI.com]][FastAPI-url]
* [![LangChain][LangChain.com]][LangChain-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running, follow these simple steps.

### Prerequisites

* Conda or Miniconda
* Poetry

### Installation

1. Check the Python version used in the repo
   ```sh
   # Step 1: check the python version used in the repo (see pyproject.toml to find it)
   conda create -n <repo-name> python=<python version it's either 3.10 or 3.11>
   ```

2. Configure Poetry to use the Conda environment
   ```sh
   # Step 2: it's generally inside $HOME/opt/miniconda3/envs/base-python310/bin/python
   poetry env use <python path to conda env created>
   ```

3. Install dependencies using Poetry
   ```sh
   # Step 3:
   poetry install
   ```

4. Set up your IDE
   ```sh
   # Step 4:
   # Change python interpreter in your IDE to use the Conda environment
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [Agent Service Toolkit](https://github.com/JoshuaC215/agent-service-toolkit)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/Ashishkumaraswamy/CodeForHer-Backend.svg?style=for-the-badge
[contributors-url]: https://github.com/Ashishkumaraswamy/CodeForHer-Backend/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/Ashishkumaraswamy/CodeForHer-Backend.svg?style=for-the-badge
[forks-url]: https://github.com/Ashishkumaraswamy/CodeForHer-Backend/network/members
[stars-shield]: https://img.shields.io/github/stars/Ashishkumaraswamy/CodeForHer-Backend.svg?style=for-the-badge
[stars-url]: https://github.com/Ashishkumaraswamy/CodeForHer-Backend/stargazers
[issues-shield]: https://img.shields.io/github/issues/Ashishkumaraswamy/CodeForHer-Backend.svg?style=for-the-badge
[issues-url]: https://github.com/Ashishkumaraswamy/CodeForHer-Backend/issues
[license-shield]: https://img.shields.io/github/license/Ashishkumaraswamy/CodeForHer-Backend.svg?style=for-the-badge
[license-url]: https://github.com/Ashishkumaraswamy/CodeForHer-Backend/blob/master/LICENSE
[product-screenshot]: codeforher_backend/assets/Code_For_Her.png
[Python.com]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://www.python.org/
[FastAPI.com]: https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white
[FastAPI-url]: https://fastapi.tiangolo.com/
[LangChain.com]: https://img.shields.io/badge/LangChain-000000?style=for-the-badge&logo=chainlink&logoColor=white
[LangChain-url]: https://python.langchain.com/
