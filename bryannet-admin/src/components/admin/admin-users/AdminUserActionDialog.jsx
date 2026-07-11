import ConfirmDialog from "../../common/ConfirmDialog";

function AdminUserActionDialog({

    open,

    loading = false,

    administrator,

    activate = true,

    onClose,

    onConfirm,

}) {

    return (

        <ConfirmDialog

            open={open}

            loading={loading}

            title={

                activate

                    ? "Activate Administrator"

                    : "Deactivate Administrator"

            }

            message={

                administrator

                    ? activate

                        ? `Activate "${administrator.username}"?`

                        : `Deactivate "${administrator.username}"?`

                    : ""

            }

            confirmText={

                activate

                    ? "Activate"

                    : "Deactivate"

            }

            onClose={onClose}

            onConfirm={onConfirm}

        />

    );

}

export default AdminUserActionDialog;