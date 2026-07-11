import React from "react";

import {
    MenuItem,
    TextField,
} from "@mui/material";

import FormDialog from "../../common/FormDialog";
import FormGrid from "../../common/FormGrid";
import FormGridItem from "../../common/FormGridItem";

const DEFAULT_FORM = {

    username: "",

    email: "",

    password: "",

    role_id: "",

};

function AdminUserForm({

    open,

    loading = false,

    administrator = null,

    roles = [],

    onClose,

    onSubmit,

}) {

    const [formData, setFormData] = React.useState(
        DEFAULT_FORM,
    );

    React.useEffect(() => {

        if (!open) {

            return;

        }

        if (administrator) {

            setFormData({

                username:
                    administrator.username,

                email:
                    administrator.email,

                password: "",

                role_id:
                    administrator.role_id,

            });

        } else {

            setFormData(
                DEFAULT_FORM,
            );

        }

    }, [

        administrator,

        open,

    ]);

    const handleChange = (
        event,
    ) => {

        const {

            name,

            value,

        } = event.target;

        setFormData(

            (previous) => ({

                ...previous,

                [name]: value,

            }),

        );

    };

    const handleSubmit = () => {

        const payload = {

            username:
                formData.username,

            email:
                formData.email,

            role_id:
                Number(
                    formData.role_id,
                ),

        };

        if (!administrator) {

            payload.password =
                formData.password;

        }

        onSubmit(
            payload,
        );

    };

    return (

        <FormDialog

            open={open}

            loading={loading}

            title={

                administrator

                    ? "Edit Administrator"

                    : "Create Administrator"

            }

            submitLabel={

                administrator

                    ? "Save Changes"

                    : "Create Administrator"

            }

            onClose={onClose}

            onSubmit={handleSubmit}

        >

            <FormGrid>

                <FormGridItem>

                    <TextField

                        fullWidth

                        required

                        name="username"

                        label="Username"

                        value={
                            formData.username
                        }

                        onChange={
                            handleChange
                        }

                    />

                </FormGridItem>

                <FormGridItem>

                    <TextField

                        fullWidth

                        required

                        type="email"

                        name="email"

                        label="Email Address"

                        value={
                            formData.email
                        }

                        onChange={
                            handleChange
                        }

                    />

                </FormGridItem>

                {!administrator && (

                    <FormGridItem>

                        <TextField

                            fullWidth

                            required

                            type="password"

                            name="password"

                            label="Password"

                            value={
                                formData.password
                            }

                            onChange={
                                handleChange
                            }

                        />

                    </FormGridItem>

                )}

                {!administrator && (

                    <FormGridItem>

                        <TextField

                            select

                            fullWidth

                            required

                            name="role_id"

                            label="Role"

                            value={
                                formData.role_id
                            }

                            onChange={
                                handleChange
                            }

                        >

                            {roles.map(
                                (role) => (

                                    <MenuItem

                                        key={
                                            role.role_id
                                        }

                                        value={
                                            role.role_id
                                        }

                                    >

                                        {
                                            role.role_name
                                        }

                                    </MenuItem>

                                ),
                            )}

                        </TextField>

                    </FormGridItem>

                )}

            </FormGrid>

        </FormDialog>

    );

}

export default AdminUserForm;