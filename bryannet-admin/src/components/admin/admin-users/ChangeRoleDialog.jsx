import {
    MenuItem,
    TextField,
} from "@mui/material";

import FormDialog from "../../common/FormDialog";

function ChangeRoleDialog({

    open,

    loading = false,

    administrator,

    roles = [],

    selectedRole,

    onRoleChange,

    onClose,

    onSubmit,

}) {

    return (

        <FormDialog

            open={open}

            loading={loading}

            title="Change Administrator Role"

            submitLabel="Save Role"

            onClose={onClose}

            onSubmit={onSubmit}

        >

            <TextField

                fullWidth

                label="Administrator"

                value={
                    administrator?.username ?? ""
                }

                InputProps={{

                    readOnly: true,

                }}

                sx={{

                    mb: 3,

                }}

            />

            <TextField

                select

                fullWidth

                required

                label="Role"

                value={selectedRole}

                onChange={onRoleChange}

            >

                {roles.map((role) => (

                    <MenuItem

                        key={role.role_id}

                        value={role.role_id}

                    >

                        {role.role_name}

                    </MenuItem>

                ))}

            </TextField>

        </FormDialog>

    );

}

export default ChangeRoleDialog;