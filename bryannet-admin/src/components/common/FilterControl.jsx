import {
    FormControl,
    MenuItem,
    Select,
} from "@mui/material";

function FilterControl({

    value,

    onChange,

    options = [],

    minWidth = 170,

}) {

    return (

        <FormControl
            size="small"
            sx={{
                minWidth,
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

    );

}

export default FilterControl;