import {
    Box,
    Divider,
    Stack,
    Typography,
} from "@mui/material";

function FormSection({

    title,

    subtitle = "",

    actions = null,

    children,

    divider = true,

    spacing = 2,

}) {

    return (

        <Box>

            {(title || subtitle || actions) && (

                <Stack
                    direction="row"
                    justifyContent="space-between"
                    alignItems="flex-start"
                    sx={{
                        mb: 2,
                    }}
                >

                    <Box>

                        {title && (

                            <Typography
                                variant="subtitle1"
                                fontWeight={700}
                            >

                                {title}

                            </Typography>

                        )}

                        {subtitle && (

                            <Typography
                                variant="body2"
                                color="text.secondary"
                                sx={{
                                    mt: 0.5,
                                }}
                            >

                                {subtitle}

                            </Typography>

                        )}

                    </Box>

                    {actions}

                </Stack>

            )}

            <Stack
                spacing={spacing}
            >

                {children}

            </Stack>

            {divider && (

                <Divider
                    sx={{
                        mt: 3,
                    }}
                />

            )}

        </Box>

    );

}

export default FormSection;