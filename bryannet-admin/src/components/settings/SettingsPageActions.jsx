import {
    Button,
    Stack,
} from "@mui/material";

import RefreshIcon from "@mui/icons-material/Refresh";
import SaveIcon from "@mui/icons-material/Save";

export default function SettingsPageActions({

    onSave,

    onReset,

    loading = false,

    saveLabel = "Save Changes",

    resetLabel = "Reset",

}) {

    return (

        <Stack

            direction="row"

            spacing={2}

            justifyContent="flex-end"

        >

            <Button

                variant="outlined"

                startIcon={<RefreshIcon />}

                onClick={onReset}

                disabled={loading}

            >

                {resetLabel}

            </Button>

            <Button

                variant="contained"

                startIcon={<SaveIcon />}

                onClick={onSave}

                disabled={loading}

            >

                {loading

                    ? "Saving..."

                    : saveLabel}

            </Button>

        </Stack>

    );

}