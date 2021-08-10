---
title: "Docs"
url: /
aliases:
    - /docs/index.html
    - /docs/Overview.html
no_list: true
---

This is the landing page! Hello :)

Lets's try out some tab panels:

{{< tabpane >}}
  {{< tab header="English" >}}
    Welcome!
  {{< /tab >}}
  {{< tab header="German" >}}
    Herzlich willkommen!
  {{< /tab >}}
  {{< tab header="Swahili" >}}
    Karibu sana!
  {{< /tab >}}
{{< /tabpane >}}

{{% pageinfo color="primary" %}}
This is a box.
{{% /pageinfo %}}

What about cards?

{{< cardpane >}}
  {{< card header="Header card 1" >}}
    Content card 1
  {{< /card >}}
  {{< card header="Header card 2" >}}
    Content card 2
  {{< /card >}}
  {{< card header="Header card 3" footer="![MendixImage](https://www.mendix.com/wp-content/uploads/accelerate-app-journey.png)">}}
    Content card 3
	We can even put images in.
  {{< /card >}}
{{< /cardpane >}}

{{< highlight Shell "linenos=table" >}}
# some code
echo "Hello World"
{{< /highlight >}}