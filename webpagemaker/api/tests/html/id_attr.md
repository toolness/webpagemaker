We want to allow users to play with CSS, which means we need to allow
use of the `id` attribute. HTML like this should be perfectly fine:

```html
<!DOCTYPE html><html><head></head><body>
<a id="blah">u</a>
<footer id="gloop">sup</footer>
</body></html>
```

Fortunately, the documents users are making are completely devoid of
JavaScript, so there's no danger in e.g. a jQuery selector going awry
and causing a security breach.
