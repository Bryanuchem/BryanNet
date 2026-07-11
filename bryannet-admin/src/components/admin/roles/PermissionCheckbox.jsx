import {

    Checkbox,

    FormControlLabel,

    Stack,

    Typography,

} from "@mui/material";

function PermissionCheckbox({

    permission,

    onChange,

}) {

    return (

        <Stack
            spacing={0.25}
            sx={{
                py: 0.75,
            }}
        >

            <FormControlLabel

                control={

                    <Checkbox

                        checked={

                            permission.enabled

                        }

                        onChange={(event) =>

                            onChange({

                                permissionId:

                                    permission.id,

                                checked:

                                    event.target.checked,

                            })

                        }

                    />

                }

                label={

                    <Typography
                        fontWeight={500}
                    >

                        {permission.name}

                    </Typography>

                }

                sx={{

                    alignItems: "flex-start",

                    m: 0,

                }}

            />

            {permission.description && (

                <Typography

                    variant="body2"

                    color="text.secondary"

                    sx={{

                        ml: 4.5,

                    }}

                >

                    {permission.description}

                </Typography>

            )}

        </Stack>

    );

}

export default PermissionCheckbox;