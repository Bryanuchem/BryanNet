import MemoryOutlinedIcon from "@mui/icons-material/MemoryOutlined";

import FormDialog from "../../common/FormDialog";
import FormSection from "../../common/FormSection";
import FormGrid from "../../common/FormGrid";
import FormGridItem from "../../common/FormGridItem";
import InfoField from "../../common/InfoField";
import BadgeChip from "../../common/BadgeChip";

function SystemActivityDetailsDialog({

    open,

    activity,

    onClose,

}) {

    if (!activity) {

        return null;

    }

    return (

        <FormDialog

            open={open}

            title="System Activity Details"

            subtitle="View complete information about this system event."

            icon={

                <MemoryOutlinedIcon

                    color="primary"

                    fontSize="large"

                />

            }

            maxWidth="md"

            submitText="Close"

            onSubmit={onClose}

            onClose={onClose}

            hideCancel

        >

            <FormSection

                title="Activity Information"

                subtitle="Details of the recorded system activity."

            >

                <FormGrid>

                    <FormGridItem md={6}>

                        <InfoField

                            label="Action"

                        >

                            {

                                activity.action

                            }

                        </InfoField>

                    </FormGridItem>

                    <FormGridItem md={6}>

                        <InfoField

                            label="Result"

                        >

                            <BadgeChip

                                status={

                                    activity.result

                                        ?.toLowerCase()

                                }

                                label={

                                    activity.result

                                }

                            />

                        </InfoField>

                    </FormGridItem>

                    <FormGridItem md={6}>

                        <InfoField

                            label="Entity"

                        >

                            {

                                activity.entity_type

                            }

                        </InfoField>

                    </FormGridItem>

                    <FormGridItem md={6}>

                        <InfoField

                            label="Target"

                        >

                            {

                                activity.target_name

                                ||

                                "-"

                            }

                        </InfoField>

                    </FormGridItem>

                    <FormGridItem>

                        <InfoField

                            label="Description"

                        >

                            {

                                activity.description

                            }

                        </InfoField>

                    </FormGridItem>

                </FormGrid>

            </FormSection>

            <FormSection

                title="Changes"

                subtitle="Recorded values associated with this activity."

            >

                <FormGrid>

                    <FormGridItem md={6}>

                        <InfoField

                            label="Old Values"

                        >

                            {

                                activity.old_values

                                    ? JSON.stringify(

                                        activity.old_values,

                                        null,

                                        2,

                                    )

                                    : "-"

                            }

                        </InfoField>

                    </FormGridItem>

                    <FormGridItem md={6}>

                        <InfoField

                            label="New Values"

                        >

                            {

                                activity.new_values

                                    ? JSON.stringify(

                                        activity.new_values,

                                        null,

                                        2,

                                    )

                                    : "-"

                            }

                        </InfoField>

                    </FormGridItem>

                </FormGrid>

            </FormSection>

            <FormSection

                title="Execution Information"

                subtitle="Information about the execution of this system event."

            >

                <FormGrid>

                    <FormGridItem md={6}>

                        <InfoField

                            label="Administrator"

                        >

                            {

                                activity.administrator

                                ||

                                "System"

                            }

                        </InfoField>

                    </FormGridItem>

                    <FormGridItem md={6}>

                        <InfoField

                            label="Session ID"

                        >

                            {

                                activity.admin_session_id

                                ??

                                "-"

                            }

                        </InfoField>

                    </FormGridItem>

                    <FormGridItem md={6}>

                        <InfoField

                            label="IP Address"

                        >

                            {

                                activity.ip_address

                                ||

                                "-"

                            }

                        </InfoField>

                    </FormGridItem>

                    <FormGridItem md={6}>

                        <InfoField

                            label="User Agent"

                        >

                            {

                                activity.user_agent

                                ||

                                "-"

                            }

                        </InfoField>

                    </FormGridItem>

                </FormGrid>

            </FormSection>

            <FormSection

                title="Record Information"

                subtitle="System activity metadata."

                divider={false}

            >

                <FormGrid>

                    <FormGridItem md={6}>

                        <InfoField

                            label="Activity ID"

                        >

                            {

                                activity.audit_log_id

                            }

                        </InfoField>

                    </FormGridItem>

                    <FormGridItem md={6}>

                        <InfoField

                            label="Created"

                        >

                            {

                                activity.created_at

                                    ? new Date(

                                        activity.created_at,

                                    ).toLocaleString()

                                    : "-"

                            }

                        </InfoField>

                    </FormGridItem>

                </FormGrid>

            </FormSection>

        </FormDialog>

    );

}

export default SystemActivityDetailsDialog;