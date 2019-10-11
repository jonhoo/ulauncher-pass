A very straightforward [pass](https://www.passwordstore.org/) extension
with fuzzy search for [Ulauncher](https://ulauncher.io/).

To install, go to "Ulauncher preferences", click "Extensions", then "Add
extension" and paste the URL https://github.com/jonhoo/ulauncher-pass.
You can also check out the repository manually into
`~/.local/share/ulauncher/extensions` if you want to make modifications
yourself.

Once the extension is installed, you can pull up passwords by typing
`pass` followed by a search string (you can configure this prefix). The
search string is fuzzy-matched against all the passwords stored in
`~/.password-store`, so you usually only need to type a few of the
letters to get a match. Selecting an entry copies the stored password to
your clipboard. That's all!
