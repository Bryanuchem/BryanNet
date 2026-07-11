import {
    FormControl,
    MenuItem,
    Select,
} from "@mui/material";

function FilterControl({

    value,

    onChange,

    options = [],

    placeholder = "Select",

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

                displayEmpty

                renderValue={(selected) => {

                    if (
                        selected === "" ||
                        selected === null ||
                        selected === undefined
                    ) {

                        return placeholder;

                    }

                    const option = options.find(

                        (item) =>
                            item.value === selected,

                    );

                    return (
                        option?.label ??
                        placeholder
                    );

                }}

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