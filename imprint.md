---
layout: page
title: Contact & Imprint
description: Imprint
#banner_image: aboutPage.jpg
---

<address>
<p>
	<strong>Contact:</strong> Daniel Vogelbacher
</p>
<p>
<strong>Address:</strong> Unterdorfstr. 57, 68753 Waghäusel, Germany<br />
<strong>E-Mail:</strong> daniel@chaospixel.com
</p>
<p>
<strong>GPG Fingerprint:</strong> F844 037D BE0E 9385 6475  B95A 9FDA 52CB 9EDE 279E
</p>
</address>

<h2>Send me a message</h2>

<form class="form-contact" id="contactform" method="POST">
    <input type="text" name="name" placeholder="Your name">
    <input type="email" name="_replyto" placeholder="Your email">
    <input type="hidden" name="_subject" value="Website contact" />
    <textarea name="message" placeholder="Your message"></textarea>
    <input type="text" name="_gotcha" style="display:none" />
    <input type="submit" value="Send">
</form>
<script>
    var contactform =  document.getElementById('contactform');
    contactform.setAttribute('action', 'https://formspree.io/' + 'daniel' + '@' + 'chaospixel' + '.' + 'com');
</script>

