# franciscorichter.github.io

Personal and research website of **Francisco Richter**  
([https://franciscorichter.github.io](https://franciscorichter.github.io))

This Jekyll site showcases my publications, teaching, and interactive
applications in mathematics, statistics, and AI.

### Tech stack

* **Jekyll & GitHub Pages** – static‑site generator + hosting  
* **Minimal Mistakes** theme – layout framework (MIT licence)  
* **Academic Pages** fork – original starting point, now substantially refactored  
* Custom SCSS, JS, and layouts developed 2023‑2025

### Credits

<<<<<<< HEAD
<<<<<<< HEAD
The site began as a fork of  
[**academicpages/academicpages.github.io**](https://github.com/academicpages/academicpages.github.io)  
by Stuart Geiger, itself based on Michael Rose’s  
[**Minimal Mistakes**](https://mmistakes.github.io/minimal-mistakes/).  
Both projects are released under the MIT Licence; those terms apply to this
repository as well. See `LICENSE` for details.

### Licence

The code and content here are released under the MIT Licence unless stated
otherwise. Please attribute appropriately if you reuse any part of the site.
=======
=======
>>>>>>> parent of 1675626 (timeline)
## To run locally (not on GitHub Pages, to serve on your own computer)

1. Clone the repository and made updates as detailed above
1. Make sure you have ruby-dev, bundler, and nodejs installed: `sudo apt install ruby-dev ruby-bundler nodejs`
1. Run `bundle clean` to clean up the directory (no need to run `--force`)
1. Run `bundle install` to install ruby dependencies. If you get errors, delete Gemfile.lock and try again.
1. Run `bundle exec jekyll liveserve` to generate the HTML and serve it from `localhost:4000` the local server will automatically rebuild and refresh the pages on change.

# Changelog -- bugfixes and enhancements

There is one logistical issue with a ready-to-fork template theme like academic pages that makes it a little tricky to get bug fixes and updates to the core theme. If you fork this repository, customize it, then pull again, you'll probably get merge conflicts. If you want to save your various .yml configuration files and markdown files, you can delete the repository and fork it again. Or you can manually patch. 

To support this, all changes to the underlying code appear as a closed issue with the tag 'code change' -- get the list [here](https://github.com/academicpages/academicpages.github.io/issues?q=is%3Aclosed%20is%3Aissue%20label%3A%22code%20change%22%20). Each issue thread includes a comment linking to the single commit or a diff across multiple commits, so those with forked repositories can easily identify what they need to patch.
<<<<<<< HEAD
>>>>>>> parent of 1675626 (timeline)
=======
>>>>>>> parent of 1675626 (timeline)
