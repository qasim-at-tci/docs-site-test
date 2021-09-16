---
title: "MM MP 3"
description: "First subsection of Mark's Portal" 
linktitle: "Mark Portal 3"
cascade:
    - banner: "This is a page banner cascaded through all sub pages"
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

### Dead Link Triggers a Warning


[Dead Link]({{< ref "dead-link" >}})

## banner

(See top of page!) For example, to show that all Mx10 documentation is in Beta.

Need to set - currently in spaces.yml, add as a (cascaded) front matter? Need to add to a partial with a switch?

## Shortcodes

The Original Docs Site versions of the shortcodes use `Page.Dir` which is deprecated.

### alert

Need to change `type` to `color` - can use any of the theme colours set in `assets/scss/_variables.scss`
Can add a "title"

{{% alert type="alert" %}}Original Alert Box - only used once on site{{% /alert %}}
{{% alert color="alert" %}}Updated Alert Box{{% /alert %}}

{{% alert type="info" %}}Original Info Box{{% /alert %}}
{{% alert color="info" %}}Updated Info Box{{% /alert %}}

{{% alert type="success" %}}Original Success Box{{% /alert %}}
{{% alert color="success" %}}Updated Success Box{{% /alert %}}

{{% alert type="warning" title="H4 - does it appear in the ToC?" %}}Original Warning Box{{% /alert %}}
{{% alert color="warning" %}}Updated Warning Box{{% /alert %}}

{{% alert type="danger" %}}Original Danger Box - Not used at all on the site{{% /alert %}}
{{% alert color="danger" %}}Updated Danger Box{{% /alert %}}

### category_block

The Category Block doesn't work and can be replaced by no_list: false - provided the category block goes at the end of the page.

{{%/* category_block */%}}

See example on [MP 3.2 - no_list]({{< ref "mark-portal-section-3-2" >}})

### Image_Container

Image container does not work, but can probably be replaced by using the `height` and `width` attributes of the Figure shortcode

{{%/* image_container width="100" */%}}[![](/attachments/docs/marks-portal/lights-static.png)](https://marketplace.mendix.com/link/studiopro/){{%/* /image_container */%}}

{{< figure src="/attachments/docs/marks-portal/lights-static.png" width="100">}}

### modelerdownloadlink

Works as expected

{{% modelerdownloadlink "9.5.0" %}}

### number_child_pages

This is used for Studio Pro release notes. Seems to give similar results to `no_list: false` Use the `weight: ` to decide the list order (which then matches the left-hand menu)

{{%/* number_child_pages sort="desc" */%}}

### snippet

New Snippet function taken from Geekdocs. What do we want the naming to be?

For example {{%/* snippet file="/static/_includes/common-section-link.md" */%}}

{{% snippet file="/static/_includes/common-section-link.md" %}}

### vidyard

Currently embedded with HTML:

```
<img
  style="width: 100%; margin: auto; display: block;"
  class="vidyard-player-embed"
  src="https://videoshare.mendix.com/watch/WZu7QtHZPjtYUTdcV58PKr?.jpg"
  data-uuid="WZu7QtHZPjtYUTdcV58PKr?"
  data-v="4"
  data-type="inline"
/>
```

Not displaying properly - do we need to add class `vidyard-player-embed` to see the video

<img
  style="width: 100%; margin: auto; display: block;"
  class="vidyard-player-embed"
  src="https://videoshare.mendix.com/watch/WZu7QtHZPjtYUTdcV58PKr?.jpg"
  data-uuid="WZu7QtHZPjtYUTdcV58PKr?"
  data-v="4"
  data-type="inline"
/>

### youtube

{{/* % youtube _QMhOmc2LKA */%}}

{{% youtube _QMhOmc2LKA %}}

### todo

{{% todo %}}[Todo will appear in Travis]{{% /todo %}}

### pageinfo

Can create a block on the page by using the Docsy {{%/* pageinfo */%}} shortcode

{{% pageinfo color="warning" %}}
This is placeholder content.
{{% /pageinfo %}}

