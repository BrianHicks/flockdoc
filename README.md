Flockdoc
========

Create example API documentation in multiple languages (like [Stripe's API
docs][stripe-api])

[stripe-api]: http://stripe.com/docs/api 

Usage
-----

### Directory

You need (roughly) this directory structure.

    ├── code
    │   ├── test.py
    │   └── test.rb
    ├── docs
    │   └── index.md
    └── layout
    │   └── index.html
    ├── static
        ├── styles.css
        └── some_img.jpg

It will be transformed into (roughly) this directory structure:

    ├── code
    │   ├── test.py.html
    │   └── test.rb.html
    ├── index.html
    └── static
        ├── some_img.jpg
        └── styles.css

### Individual Files

For code, just write code as normal. Flockdoc will try to take care of
formatting for you (including multi-line comments, aren't you lucky!) The
output will look a little like [Docco][docco].

For markdown, think [Jekyll][jekyll]: header with layout specified, and then
your code. YAML header with Markdown body. Example:

    title: Test
    context:
      key: value
    ---
    This is a test document with a key: {{ key }}

Documents are passed through Jinja2 rendering before they are output.
