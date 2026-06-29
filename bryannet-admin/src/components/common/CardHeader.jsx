import {
    Box,
    FormControl,
    MenuItem,
    Select,
    Typography,
} from "@mui/material";

function CardHeader({
    title,
    value,
    onChange,
    options = [],
}) {

    return (

        <Box
            display="flex"
            justifyContent="space-between"
            alignItems="center"
            mb={3}
        >

            <Typography
                variant="h6"
                fontWeight={600}
            >
                {title}
            </Typography>

            {value && (

                <FormControl
                    size="small"
                    sx={{
                        minWidth: 170,
                    }}
                >

                    <Select
                        value={value}
                        onChange={onChange}
                    >

                        {options.map((option) => (

                            <MenuItem
                                key={option.value}
                                value={option.value}
                            >
                                {option.label}
                            </MenuItem>

                        ))}

                    </Select>

                </FormControl>

            )}

        </Box>

    );

}

export default CardHeader;