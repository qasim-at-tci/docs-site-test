---
title: "MM MP 3"
description: "First subsection of Mark's Portal" 
no_list: false
linktitle: "Mark Portal 3"
#tags: ["These", "are", "Example", "Tags"]
# weight: 10
#notoc: true
#layout: wide
#draft: true
#toc-level: "3"as
#sitemap: false (remove from Google sitemap)
#disable_sitemap: true (also remove from Google bot)
#nosearch: true (remove from Algolia)
# aliases:
#   - /xyzzy.html
---

## Introduction

This page uses all the existing shortcodes from Mendix Docs to see what Docsy produces, and what Docsy/HUGO codes could be used in their place.

### linktitle:

Uses linktitle: – menu is sorted by linktitle:, not by title:

## Shortcodes

The Original Docs Site versions of the shortcodes use `Page.Dir` which is deprecated.

### alert

Need to change type to color - can use any of the theme colours set in `assets/scss/_variables.scss`
Can add a "title"

{{% alert type="alert" %}}Original Alert Box - only used once on site{{% /alert %}}
{{% alert color="warning" %}}Updated Warning Box{{% /alert %}}

{{% alert type="info" %}}Original Info Box{{% /alert %}}
{{% alert color="info" %}}Updated Info Box{{% /alert %}}

{{% alert type="success" %}}Original Success Box{{% /alert %}}
{{% alert color="success" %}}Updated Success Box{{% /alert %}}

{{% alert type="warning" %}}Original Warning Box{{% /alert %}}
{{% alert color="warning" %}}Updated Warning Box{{% /alert %}}

{{% alert type="danger" %}}Original Danger Box - Not used at all on the site{{% /alert %}}
{{% alert color="danger" %}}Updated Danger Box{{% /alert %}}

### category_block

The Category Block doesn't work and can probably be replaced by no_list: false - provided the category block goes at the end of the page.

{{%/* category_block */%}}

### Image_Container

Image container does not work, but can probably be replaced by using the `height` and `width` attributes of the Figure shortcode

{{%/* image_container width="100" */%}}[![](/attachments/docs/marks-portal/lights-static.png)](https://marketplace.mendix.com/link/studiopro/){{%/* /image_container */%}}

{{< figure src="/attachments/docs/marks-portal/lights-static.png" width="100">}}

### modelerdownloadlink

Works as expected

{{% modelerdownloadlink "9.5.0" %}}

### number_child_pages

{{%/* number_child_pages sort="desc" */%}}

### snippet

{{%/* snippet file="refguide/common-section-link.md" */%}}

### youtube

{{% youtube _QMhOmc2LKA %}}

### todo

{{% todo %}}[Todo will appear in Travis]{{% /todo %}}
