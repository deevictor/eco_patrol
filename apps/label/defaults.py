from mezzanine.conf import register_setting


register_setting(
    name='RICHTEXT_ALLOWED_TAGS',
    append=True,
    default=("iframe",),
)

register_setting(
    name='RICHTEXT_FILTER_LEVEL',
    default=2,
)

register_setting(
    name='TINYMCE_SETUP_JS',
    default='js/tinymce_setup.js',
)

register_setting(
    name='COMMENT_PREVIEW_SIZE',
    label='Размер превью комментариев',
    editable=True,
    default=20,
)
