import {
    Card,
    CardContent,
    Divider,
    Stack,
    Typography,
} from "@mui/material";

function SectionCard({

    title,

    subtitle = "",

    actions = null,

    children,

}) {

    return (

        <Card
            elevation={0}
        >

            {(title || subtitle || actions) && (

                <>

                    <CardContent>

                        <Stack

                            direction="row"

                            justifyContent="space-between"

                            alignItems="flex-start"

                        >

                            <Stack>

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

                                    >

                                        {subtitle}

                                    </Typography>

                                )}

                            </Stack>

                            {actions}

                        </Stack>

                    </CardContent>

                    <Divider />

                </>

            )}

            <CardContent>

                {children}

            </CardContent>

        </Card>

    );

}

export default SectionCard;