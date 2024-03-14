<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/mattalexanderfields/Alfred_wf_Linear">
    <img src="images/logo.avif" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">Linear Workflow for Alfred</h3>

  <p align="center">
    Create issues from the Alfred UI
    <br />
    <a href="https://github.com/mattalexanderfields/Alfred_wf_Linear"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/mattalexanderfields/Alfred_wf_Linear">View Demo</a>
    ·
    <a href="https://github.com/mattalexanderfields/Alfred_wf_Linear/issues">Report Bug</a>
    ·
    <a href="https://github.com/mattalexanderfields/Alfred_wf_Linear/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

Linear is a modern issue tracking and project management tool that helps software teams ship better products, faster. It provides a streamlined interface for tracking issues, managing projects, and collaborating with your team.

This Alfred Workflow is designed to make it easy to create new issues directly from Alfred (a productivity application for macOS) and send them to your Linear account. Instead of having to switch to the Linear web app or manually create issues, you can quickly capture and send issues as they come up, right from your desktop.

Here's a more detailed overview of what this workflow enables:

Link Your Linear Account
The workflow allows you to authenticate and link your Linear account credentials. This connects Alfred to your Linear projects and workspaces.

Create New Issues Quickly
With a simple keyword or hotkey, you can bring up the workflow and start creating a new issue. The workflow will prompt you for the issue title

Send Issues Instantly
Once you've entered all the details, the workflow will instantly create the new issue in your linked Linear team. No more context switching or manual entry.

Increased Productivity
By reducing the friction to create and track issues, this workflow aims to boost your productivity. You can capture issues and ideas as they occur, without losing focus or context on your current task.

The overall goal is to provide a seamless way to integrate Linear's powerful issue tracking capabilities into your existing workflow, leveraging Alfred's speed and accessibility. This can be particularly useful for developers, QA engineers, project managers, or anyone who needs to frequently create and manage issues or tasks within their software development lifecycle.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

[![Alfred][Alfred-shield]][Alfred-url]
[![Python][Python-shield]][Python-url]



<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->

## Getting Started

1. **Open Alfred Preferences**
   - Launch the Alfred app on your Mac.
   - Click on the "Alfred Preferences" menu option or use the keyboard shortcut `cmd + ,` to open the preferences window.

2. **Navigate to the Workflows Section**
   - In the preferences window, click on the "Workflows" tab located on the left sidebar.

3. **Open the Alfred Gallery**
   - In the Workflows section, click on the "Add Workflow" button at the bottom.
   - This will open the Alfred Gallery, which is a collection of community-created workflows that you can install.

4. **Search for the Linear Issue Maker**
   - In the search bar at the top of the Alfred Gallery, type "Linear Issue Maker" to find the workflow.
   - The Linear Issue Maker should appear in the search results.

5. **Install the Linear Issue Maker**
   - Click on the "Install" button next to the Linear Issue Maker to begin the installation process.
   - Alfred may prompt you to grant certain permissions or provide your system password to complete the installation.

6. **Configure the Linear Issue Maker**
   - After installation, the Linear Issue Maker will be listed in the Workflows section of Alfred Preferences.
   - Click on the Linear Issue Maker to view its configuration options.
   - You will need to provide your personal API key and team UUID from Linear to authenticate and connect the workflow.
   - Follow the instructions within the workflow to enter these credentials.

7. **Start Using the Linear Issue Maker**
   - Once configured, you can invoke the Linear Issue Maker by typing the designated keyword (e.g., "linear issue") in Alfred's search bar.
   - The workflow will provide actions and features related to creating new issues in Linear directly from Alfred.

Please note that providing your personal API key and team UUID is a required step to ensure the Linear Issue Maker can authenticate and interact with your Linear account and team correctly.




### Installation

1. Go to the [Alfred Homepage](https://www.alfredapp.com/)[1]
2. Select the "Alfred Gallery" tab
3. Search for "linear issue maker" in the Alfred Gallery search bar  
4. Find the "Linear Issue Maker Workflow" in the search results
5. Click the "Install" button next to the Linear Issue Maker workflow
6. Alfred will prompt you to confirm installing the workflow. Click "Install" to proceed.
7. Once installed, you can configure the Linear Issue Maker workflow by:
   - Right-clicking on the workflow name in Alfred's sidebar and selecting "Configure..."[2]
   - Or clicking "Configure Workflow..." under the workflow's name in Alfred Preferences[2]
8. Follow any configuration prompts to set up required settings like your Linear API key, project, etc.[1][3]

The Linear Issue Maker workflow allows you to quickly create new issues in your Linear project from Alfred. By configuring it with your Linear account details, you can streamline your issue tracking workflow directly from Alfred's launcher.[1][3]

If you need any help configuring or using the Linear Issue Maker workflow, you can check the official Alfred Forum for support from the community.[2][4]

Citations:
[1] https://linear.app/docs/configuring-workflows
[2] https://www.alfredapp.com/workflows/
[3] https://linear.app
[4] https://www.alfredapp.com/blog/guides-and-tutorials/create-your-own-workflows/

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->


## Usage

This Alfred workflow allows you to quickly create linear issues from your desktop using a simple keyword and text input.

1. Invoke the workflow by typing the keyword `li` followed by a space.
2. Enter the title or description of the issue you want to create.
3. Press `Enter` to submit the input.

The workflow will automatically create a new linear issue with the provided title or description.

### Examples

- `li Add support for dark mode` - Creates a new issue titled "Add support for dark mode".
- `li Fix bug in login flow: Users are unable to reset their passwords` - Creates a new issue with the detailed description.

You can also use the `li` keyword without any text to open the linear web app directly. (not yet implemented)


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/mattalexanderfields/Alfred_wf_Linear/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>





<!-- CONTACT -->
## Contact

[@theseapriest](https://twitter.com/theseapriest) - theseapriest@gmail.com

Project Link: [https://github.com/mattalexanderfields/Alfred_wf_Linear](https://github.com/mattalexanderfields/Alfred_wf_Linear)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [joeynotjoe](https://github.com/joeynotjoe) for fixing major headaches


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/mattalexanderfields/Alfred_wf_Linear.svg?style=for-the-badge
[contributors-url]: https://github.com/mattalexanderfields/Alfred_wf_Linear/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/mattalexanderfields/Alfred_wf_Linear.svg?style=for-the-badge
[forks-url]: https://github.com/mattalexanderfields/Alfred_wf_Linear/network/members
[stars-shield]: https://img.shields.io/github/stars/mattalexanderfields/Alfred_wf_Linear.svg?style=for-the-badge
[stars-url]: https://github.com/mattalexanderfields/Alfred_wf_Linear/stargazers
[issues-shield]: https://img.shields.io/github/issues/mattalexanderfields/Alfred_wf_Linear.svg?style=for-the-badge
[issues-url]: https://github.com/mattalexanderfields/Alfred_wf_Linear/issues
[license-shield]: https://img.shields.io/github/license/mattalexanderfields/Alfred_wf_Linear.svg?style=for-the-badge
[license-url]: https://github.com/mattalexanderfields/Alfred_wf_Linear/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/linkedin_username
[product-screenshot]: images/screenshot.png
[Alfred-url]: https://www.alfredapp.com/
[Alfred-shield]: https://img.shields.io/badge/alfred-black?style=for-the-badge&logo=alfred&logoColor=%235C1F87
[Python-url]: https://www.python.org/
[Python-shield]: https://img.shields.io/badge/python-black?style=for-the-badge&logo=python&logoColor=%235C1F87
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 