import {
    Box,
    Typography,
} from "@mui/material";

import Button from "@mui/material/Button";

function PageHeader({

    title,

    subtitle,

    actions = null,

    actionLabel,

    actionIcon,

    onAction,

}) {

    return (

        <Box
            sx={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "flex-start",
                flexWrap: "wrap",
                gap: 2,
                mb: 4,
            }}
        >

            <Box>

                <Typography
                    variant="h4"
                    fontWeight={700}
                >
                    {title}
                </Typography>

                {subtitle && (

                    <Typography
                        variant="body1"
                        color="text.secondary"
                        sx={{
                            mt: 0.5,
                        }}
                    >
                        {subtitle}
                    </Typography>

                )}

            </Box>

                {(actions || actionLabel) && (

                    <Box
                        sx={{
                            display: "flex",
                            alignItems: "center",
                            gap: 1.5,
                        }}
                    >

                        {actions ?? (

                            <Button

                                variant="contained"

                                startIcon={actionIcon}

                                onClick={onAction}

                            >

                                {actionLabel}

                            </Button>

                        )}

                    </Box>

                )}

        </Box>

    );

}

export default PageHeader;