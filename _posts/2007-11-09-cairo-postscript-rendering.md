Cairo PostScript rendering
==========================

I am trying to render vector graphics with alpha blending. Too bad,
PostScript, even Level 3, does not support alpha blending. This means
that if you want to draw two objects (say, circles) in PostScript and
you want to make them look as they are alpha blended you have to do
\"some\" trick. An example:

-   draw the first, then the second object (which will overlap and
    overwrite the first) with proper colors (considering the background
    color)
-   calculate the intersection between the two areas
-   calculate the blended color, considering the transparency level of
    the two and the background color
-   draw the intersection part with the blended color

This of course gets more and more complex as more objects overlap along
the z-axis (say, a line, a circle, two rectangles and a spline curve).
For all of them you have to consider the stacking, how they overlap,
decompose the overlapping parts properly, compute the proper colors of
each intersecting region, draw all the parts in the proper order (so
they stack properly when rendered). This is not trivial.

For this reason, I was considering [Cairo](http://cairographics.org),
assuming that they solved this problem. After a little tinkering I found
out that even Cairo gives up in rendering PostScript vector graphics
with alpha blending. For example, this code draws non-blended circles
(alpha = 1.0), producing a vector based PostScript

```c
int main (int argc, char *argv[]) {
        cairo_surface_t *surface;
        cairo_t *cr;
        char *filename = "image.ps";

        surface = (cairo_surface_t *)cairo_ps_surface_create (filename, 80.0, 80.0);
        cr = cairo_create (surface);

        cairo_set_source_rgba (cr, 1.0, 0.0, 0.0, 1.0);
        cairo_set_line_width (cr, 1.0);
        cairo_set_fill_rule (cr, CAIRO_FILL_RULE_WINDING);

        cairo_arc(cr, 20.0, 20.0, 10.0, 0.0, 2*M_PI);
        cairo_fill(cr);
        cairo_stroke (cr);

        cairo_set_source_rgba (cr, 0.0, 0.0, 1.0, 1.0);
        cairo_arc(cr, 30.0, 20.0, 10.0, 0.0, 2*M_PI);
        cairo_fill(cr);
        cairo_stroke (cr);

        cairo_set_source_rgba (cr, 0.0, 1.0, 0.0, 1.0);
        cairo_arc(cr, 25.0, 28.6, 10.0, 0.0, 2*M_PI);
        cairo_fill(cr);
        cairo_stroke (cr);

        cairo_destroy (cr);
        cairo_surface_destroy (surface);

        return 0;
}
```

However, if you replace

```c
cairo_set_source_rgba (cr, 1.0, 0.0, 0.0, 1.0);
```

with

```c
cairo_set_source_rgba (cr, 1.0, 0.0, 0.0, 0.5);
```

consequently enabling the need for alpha blending, things change. The
final PostScript file contains a rastered image, not a vector
representation. If you render it using the PDF backend, the image
contains vector-based graphics with blending. I\'m not really into the
PDF format, but this fact hints at native alpha blending support.

The picture show the three different cases. From left to right,
PostScript backend without alpha blending, PostScript backend with alpha
blending, and PDF backend with alpha blending.

![image](http://forthescience.org/blog/wp-content/uploads/2007/11/cairo_rendering.png){.align-center
width="400px"}

The PDF output was obtained by changing the line

```c
surface = (cairo_surface_t *)cairo_ps_surface_create (filename, 80.0, 80.0);
```

to

```c
surface = (cairo_surface_t *)cairo_pdf_surface_create (filename, 80.0, 80.0);
```

and of course changing also the file name accordingly. Please note that
both PostScript images were converted to PDF using ps2pdf before being
displayed: due to some setup problems on my mac, I am not able to open
PostScript files directly (which are converted by Preview.app to PDF
anyway). This however does not affect the conclusion, which is also
confirmed by peeking into the generated PostScript files with an editor.

The raster, quite low quality nature of the PostScript with alpha
blending is evident. Apparently, Cairo renders what looks like a JPEG
image, and then includes it using DataSource (See [PostScript reference
manual](http://partners.adobe.com/public/developer/en/ps/psrefman.pdf),
Section 4.10).

Concluding, from my findings it looks like Cairo is not able produce a
PostScript vectorial representation containing alpha blending. It must
resort to a raster representation, therefore losing all the advantages
of a vector format.

Despite this, I think Cairo is a very nice and powerful library to
render vector graphics in a programmatic way. Kudos to the implementors!
