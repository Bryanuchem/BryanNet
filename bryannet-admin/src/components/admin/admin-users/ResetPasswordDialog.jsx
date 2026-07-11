import {
    TextField,
    Typography,
} from "@mui/material";

import {
    useState,
} from "react";

import FormDialog from "../../common/FormDialog";

function ResetPasswordDialog({

    open,

    loading = false,

    administrator,

    onClose,

    onSubmit,

}) {

    const [password, setPassword] = useState("");

    const handleClose = () => {

        setPassword("");

        onClose();

    };

    const handleSubmit = () => {

        onSubmit(
            password,
        );

        setPassword("");

    };

    return (

        <FormDialog

            open={open}

            loading={loading}

            title="Reset Password"

            submitLabel="Reset Password"

            onClose={handleClose}

            onSubmit={handleSubmit}

        >

            <Typography
                variant="body2"
                color="text.secondary"
                sx={{
                    mb: 3,
                }}
            >

                Set a new password for{" "}

                <strong>

                    {administrator?.username}

                </strong>

                .

            </Typography>

            <TextField

                fullWidth

                required

                autoFocus

                type="password"

                label="New Password"

                value={password}

                onChange={(event) =>

                    setPassword(
                        event.target.value,
                    )

                }

            />

        </FormDialog>

    );

}

export default ResetPasswordDialog;