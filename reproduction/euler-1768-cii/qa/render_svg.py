"""Optional visual QA using preinstalled librsvg/cairo, not a runtime dependency."""
import ctypes as c
from pathlib import Path

root = Path(__file__).resolve().parents[1]
rsvg = c.CDLL('librsvg-2.so.2')
cairo = c.CDLL('libcairo.so.2')
gobject = c.CDLL('libgobject-2.0.so.0')

class Rectangle(c.Structure):
    _fields_ = [(name, c.c_double) for name in ('x', 'y', 'width', 'height')]

rsvg.rsvg_handle_new_from_file.argtypes = [c.c_char_p, c.POINTER(c.c_void_p)]
rsvg.rsvg_handle_new_from_file.restype = c.c_void_p
rsvg.rsvg_handle_render_document.argtypes = [c.c_void_p, c.c_void_p, c.POINTER(Rectangle), c.POINTER(c.c_void_p)]
rsvg.rsvg_handle_render_document.restype = c.c_int
cairo.cairo_image_surface_create.argtypes = [c.c_int, c.c_int, c.c_int]
cairo.cairo_image_surface_create.restype = c.c_void_p
cairo.cairo_create.argtypes = [c.c_void_p]
cairo.cairo_create.restype = c.c_void_p
cairo.cairo_surface_write_to_png.argtypes = [c.c_void_p, c.c_char_p]
cairo.cairo_surface_write_to_png.restype = c.c_int
cairo.cairo_destroy.argtypes = [c.c_void_p]
cairo.cairo_surface_destroy.argtypes = [c.c_void_p]
gobject.g_object_unref.argtypes = [c.c_void_p]

error = c.c_void_p()
handle = rsvg.rsvg_handle_new_from_file(bytes(root / 'results/strict-overlap.svg'), c.byref(error))
if not handle:
    raise RuntimeError('librsvg could not load the SVG')
surface = cairo.cairo_image_surface_create(0, 900, 500)
context = cairo.cairo_create(surface)
viewport = Rectangle(0, 0, 900, 500)
try:
    if not rsvg.rsvg_handle_render_document(handle, context, c.byref(viewport), c.byref(error)):
        raise RuntimeError('librsvg could not render the SVG')
    target = root / 'results/strict-overlap.png'
    status = cairo.cairo_surface_write_to_png(surface, bytes(target))
    if status:
        raise RuntimeError(f'cairo PNG status={status}')
    print(f'Rendered {target.name}: 900 x 500 with system librsvg-2.so.2 and libcairo.so.2')
finally:
    cairo.cairo_destroy(context)
    cairo.cairo_surface_destroy(surface)
    gobject.g_object_unref(handle)
