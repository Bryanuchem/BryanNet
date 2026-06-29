import {
    Stack,
    Typography,
} from "@mui/material";

function DetailItem({

    label,

    value,

    direction = "row",

    alignItems,

    spacing = 2,

    minWidth = 140,

}) {

    const isVertical =
        direction === "column";

    return (

        <Stack

            direction={direction}

            spacing={spacing}

            alignItems={
                alignItems ||

                (
                    isVertical
                        ? "flex-start"
                        : "center"
                )
            }

        >

            <Typography

                variant="body2"

                color="text.secondary"

                sx={{

                    minWidth: isVertical
                        ? "auto"
                        : minWidth,

                    fontWeight: 600,

                    flexShrink: 0,

                }}

            >

                {label}

            </Typography>

            <Typography

                variant="body1"

                sx={{

                    wordBreak: "break-word",

                    flex: 1,

                }}

                component="div"

            >

                {value ?? "-"}

            </Typography>

        </Stack>

    );

}

export default DetailItem;