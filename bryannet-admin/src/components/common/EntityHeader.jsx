import {
    Box,
    Stack,
    Typography,
} from "@mui/material";

function EntityHeader({

    title,

    subtitle,

    avatar = null,

    status = null,

    actions = null,

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

                {avatar}

                <Box>

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

                </Box>

            </Stack>

            <Stack

                direction="row"

                spacing={1}

                alignItems="center"

            >

                {status}

                {actions}

            </Stack>

        </Stack>

    );

}

export default EntityHeader;