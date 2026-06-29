import {
    Button,
    CircularProgress,
    Dialog,
    DialogActions,
    DialogContent,
    DialogTitle,
    Divider,
    Stack,
    Typography,
} from "@mui/material";

function DefaultHeader({

    title,

    subtitle,

    icon,

    actions,

}) {

    return (

        <Stack
            direction="row"
            justifyContent="space-between"
            alignItems="flex-start"
            spacing={2}
        >

            <Stack
                direction="row"
                spacing={2}
                alignItems="center"
            >

                {icon}

                <Stack spacing={0.5}>

                    <Typography
                        variant="h6"
                        fontWeight={700}
                    >

                        {title}

                    </Typography>

                    {subtitle && (

                        <Typography
                            variant="body2"
                            color="text.secondary"
                        >

                            {subtitle}

                        </Typography>

                    )}

                </Stack>

            </Stack>

            {actions}

        </Stack>

    );

}

function DefaultFooter({

    loading,

    disableSubmit,

    submitText,

    loadingText,

    cancelText,

    submitColor,

    submitVariant,

    submitIcon,

    showCancel,

    onSubmit,

    onClose,

}) {

    return (

        <>

            {showCancel && (

                <Button

                    onClick={onClose}

                    disabled={loading}

                >

                    {cancelText}

                </Button>

            )}

            <Button

                variant={submitVariant}

                color={submitColor}

                onClick={onSubmit}

                disabled={
                    loading ||
                    disableSubmit
                }

                startIcon={

                    loading

                        ? (

                            <CircularProgress
                                size={18}
                                color="inherit"
                            />

                        )

                        : submitIcon

                }

            >

                {loading
                    ? loadingText
                    : submitText}

            </Button>

        </>

    );

}

function FormDialog({

    open,

    children,

    loading = false,

    maxWidth = "md",

    fullWidth = true,

    title,

    subtitle = "",

    icon = null,

    header = null,

    headerActions = null,

    footer = null,

    contentSx = {},

    submitText = "Save",

    loadingText = "Saving...",

    cancelText = "Cancel",

    submitColor = "primary",

    submitVariant = "contained",

    submitIcon = null,

    disableSubmit = false,

    showCancel = true,

    dividers = false,

    onSubmit,

    onClose,

}) {

    return (

        <Dialog

            open={open}

            maxWidth={maxWidth}

            fullWidth={fullWidth}

            onClose={
                loading
                    ? undefined
                    : onClose
            }

        >

            <DialogTitle>

                {header || (

                    <DefaultHeader

                        title={title}

                        subtitle={subtitle}

                        icon={icon}

                        actions={headerActions}

                    />

                )}

            </DialogTitle>

            <Divider />

            <DialogContent

                dividers={dividers}

                sx={{

                    py: 3,

                    ...contentSx,

                }}

            >

                <Stack
                    spacing={4}
                >

                    {children}

                </Stack>

            </DialogContent>

            <Divider />

            <DialogActions
                sx={{
                    px: 3,
                    py: 2,
                }}
            >

                {footer || (

                    <DefaultFooter

                        loading={loading}

                        disableSubmit={disableSubmit}

                        submitText={submitText}

                        loadingText={loadingText}

                        cancelText={cancelText}

                        submitColor={submitColor}

                        submitVariant={submitVariant}

                        submitIcon={submitIcon}

                        showCancel={showCancel}

                        onSubmit={onSubmit}

                        onClose={onClose}

                    />

                )}

            </DialogActions>

        </Dialog>

    );

}

export default FormDialog;