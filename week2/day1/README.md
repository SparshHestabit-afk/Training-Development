#                                               HestaBit Training Development
#                                                       Week 2 - Day 1

# Semantic News Blog Webpage

## Overview
This project documents the creation of a **News Blog Webpage** built entirely using **semantic HTML5**.  
The emphasis of this task was not on styling or interactivity, but on understanding how proper HTML structure, semantics, and accessibility principles are applied in real-world web pages.

The layout follows a standard news/blog format, including navigation, featured headlines, article listings, sidebar content, and a footer with a feedback form. The implementation reflects how content-driven websites are structured before visual styling is applied.

---

## Purpose of the Task
The main purpose of this exercise was to:
- Practice writing **meaningful and semantic HTML**
- Understand how webpage structure impacts **readability and accessibility**
- Learn how **HTML5 native validation** works without JavaScript
- Create a layout that resembles a real news website from an industry perspective

---

## Structural Breakdown and Semantics

### Header (`<header>`)
The header represents the top section of the webpage and introduces the website.

In this project, it contains:
- The website title
- The primary navigation menu

Using a `<header>` helps clearly define the starting point of the page and allows assistive technologies to quickly identify introductory content.

---

### Navigation (`<nav>`)
The navigation element is used to group all major navigation links.

It appears in:
- The main header (primary site navigation)
- The footer (secondary navigation links)

This makes navigation predictable and improves both usability and accessibility.

---

### Main Content (`<main>`)
The `<main>` element wraps the core content of the webpage.

All news-related content, including articles and supporting sections, is placed inside `<main>`.  
This ensures that screen readers and other assistive tools can skip repetitive elements and focus directly on the primary content.

---

### Sections (`<section>`)
Sections are used to logically group related content.

They are used for:
- Featured headlines
- Introductory text
- Grouping articles and sidebar content
- Sidebar widgets
- Footer feedback area

Each section serves a clear purpose and keeps the document organized.

---

### Articles (`<article>`)
Each news item is marked using the `<article>` element.

Articles are:
- Independent
- Self-contained
- Reusable outside the context of the page

This reflects how real news platforms structure blog posts and news entries.

---

### Sidebar (`<aside>`)
The `<aside>` element is used for supplementary content.

In this project, it contains:
- Search functionality
- Latest updates
- News categories
- Trending topics

This content supports the main articles without interrupting their flow.

---

### Footer (`<footer>`)
The footer concludes the webpage and provides additional information and interaction options.

It includes:
- Footer navigation links
- Copyright details
- A feedback form for user input

Placing the feedback form in the footer aligns with common design practices used on content-driven websites.

---

## Feedback Form Explanation

### Form (`<form>`)
The form allows users to submit feedback related to the website or its content.

It is implemented using semantic and accessible form elements only.

---

### Grouping (`<fieldset>` and `<legend>`)
Form fields are grouped using `<fieldset>`, with `<legend>` providing context.

This improves clarity and ensures better accessibility, especially for screen readers.

---

### Labels (`<label>`)
Each input field is paired with a label.

This:
- Improves form usability
- Helps users understand what information is required
- Is essential for accessible form design

---

### Input Elements
The form uses:
- Text input for name
- Email input for contact information
- Select dropdown for feedback type
- Textarea for detailed feedback
- Checkbox for user consent

Each input type is chosen based on the nature of data being collected.

---

## Validation Approach
The form uses **native HTML5 validation**, without relying on JavaScript.

The following validations are implemented:

| Validation | Method Used | Reason |
|----------|------------|--------|
| Mandatory fields | `required` | Prevents incomplete submissions |
| Input length | `minlength`, `maxlength` | Ensures meaningful input |
| Email format | `type="email"` | Validates email structure |
| Dropdown selection | Empty default option | Forces a valid choice |
| User consent | Required checkbox | Ensures acknowledgment |

---

## Accessibility Considerations
The following practices were followed:
- Use of semantic HTML landmarks
- Clear heading hierarchy
- Proper label-to-input association
- Logical document flow
- Descriptive sectioning

These choices help improve the experience for users relying on assistive technologies.

---

## Technologies Used
- HTML5
- Browser-native validation
- No CSS or JavaScript (structure-focused task)

---

## Key Takeaways
Through this task:
- The importance of semantic HTML became clear
- Accessibility considerations were applied in practice
- Native HTML validation was understood and implemented
- A realistic news/blog structure was created from scratch

---

## Possible Improvements
- Adding CSS for layout and responsiveness
- Enhancing validation using JavaScript
- Connecting the feedback form to a backend service
- Implementing pagination and dynamic search

---

## Usage Notes
This project is intended strictly for **learning and training purposes**, focusing on structure, semantics, and accessibility rather than design.

---

