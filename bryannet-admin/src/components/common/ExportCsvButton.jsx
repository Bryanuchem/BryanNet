import Button from "@mui/material/Button";

import DownloadIcon from "@mui/icons-material/Download";


function ExportCsvButton({

    filename,

    rows,

    columns,

    disabled = false,

}) {

    const escapeValue = (
        value,
    ) => {

        if (
            value === null ||
            value === undefined
        ) {

            return "";

        }

        return `"${String(value)
            .replaceAll(
                '"',
                '""',
            )}"`;

    };

    const exportCsv = () => {

        if (
            disabled ||
            rows.length === 0
        ) {

            return;

        }

        const header = columns.map(
            (column) => column.label,
        );

        const body = rows.map(
            (row) =>

                columns.map(
                    (column) => {

                        const rawValue =
                            row[column.key];

                        const value =
                            column.formatter
                                ? column.formatter(
                                      rawValue,
                                      row,
                                  )
                                : rawValue;

                        return escapeValue(
                            value,
                        );

                    },
                ),

        );

        const csv = [

            header.join(","),

            ...body.map(
                (row) =>
                    row.join(","),
            ),

        ].join("\n");

        const blob = new Blob(

            [csv],

            {
                type: "text/csv;charset=utf-8;",
            },

        );

        const url =
            URL.createObjectURL(
                blob,
            );

        const link =
            document.createElement(
                "a",
            );

        link.href = url;

        link.download = `${filename}.csv`;

        document.body.appendChild(
            link,
        );

        link.click();

        document.body.removeChild(
            link,
        );

        URL.revokeObjectURL(
            url,
        );

    };

    return (

        <Button
            variant="outlined"
            startIcon={
                <DownloadIcon />
            }
            onClick={exportCsv}
            disabled={
                disabled ||
                rows.length === 0
            }
            sx={{
                whiteSpace: "nowrap",
                height: 40,
            }}
        >

            Export CSV

        </Button>

    );

}

export default ExportCsvButton;