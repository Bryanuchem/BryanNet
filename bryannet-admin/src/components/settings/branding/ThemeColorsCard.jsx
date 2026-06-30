import {
  Box,
  Card,
  CardContent,
  Grid,
  Stack,
  TextField,
  Typography,
} from "@mui/material";

export default function ThemeColorsCard({
  settings,
  onChange,
}) {
  return (
    <Card
      elevation={0}
      sx={{
        border: (theme) => `1px solid ${theme.palette.divider}`,
        borderRadius: 3,
      }}
    >
      <CardContent>
        <Stack spacing={3}>
          <Typography variant="h6">
            Theme Colors
          </Typography>

          <Grid container spacing={3}>
            <Grid
              size={{
                xs: 12,
                md: 4,
              }}
            >
              <TextField
                fullWidth
                type="color"
                label="Primary Color"
                value={settings.primaryColor}
                onChange={(event) =>
                  onChange(
                    "primaryColor",
                    event.target.value
                  )
                }
                InputLabelProps={{
                  shrink: true,
                }}
              />
            </Grid>

            <Grid
              size={{
                xs: 12,
                md: 4,
              }}
            >
              <TextField
                fullWidth
                type="color"
                label="Secondary Color"
                value={settings.secondaryColor}
                onChange={(event) =>
                  onChange(
                    "secondaryColor",
                    event.target.value
                  )
                }
                InputLabelProps={{
                  shrink: true,
                }}
              />
            </Grid>

            <Grid
              size={{
                xs: 12,
                md: 4,
              }}
            >
              <TextField
                fullWidth
                type="color"
                label="Accent Color"
                value={settings.accentColor}
                onChange={(event) =>
                  onChange(
                    "accentColor",
                    event.target.value
                  )
                }
                InputLabelProps={{
                  shrink: true,
                }}
              />
            </Grid>

            <Grid size={12}>
              <Box
                sx={{
                  mt: 1,
                  p: 3,
                  borderRadius: 2,
                  border: (theme) =>
                    `1px solid ${theme.palette.divider}`,
                  display: "flex",
                  justifyContent: "center",
                  alignItems: "center",
                  gap: 2,
                }}
              >
                <Box
                  sx={{
                    width: 48,
                    height: 48,
                    borderRadius: "50%",
                    bgcolor: settings.primaryColor,
                    border: "1px solid",
                    borderColor: "divider",
                  }}
                />

                <Box
                  sx={{
                    width: 48,
                    height: 48,
                    borderRadius: "50%",
                    bgcolor: settings.secondaryColor,
                    border: "1px solid",
                    borderColor: "divider",
                  }}
                />

                <Box
                  sx={{
                    width: 48,
                    height: 48,
                    borderRadius: "50%",
                    bgcolor: settings.accentColor,
                    border: "1px solid",
                    borderColor: "divider",
                  }}
                />
              </Box>
            </Grid>
          </Grid>
        </Stack>
      </CardContent>
    </Card>
  );
}