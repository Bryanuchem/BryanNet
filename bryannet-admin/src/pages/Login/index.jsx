import { useState } from "react";
import { useNavigate } from "react-router-dom";

import {
    Alert,
    Box,
    Button,
    Card,
    Checkbox,
    CircularProgress,
    FormControlLabel,
    Grid,
    IconButton,
    InputAdornment,
    Stack,
    TextField,
    Typography,
} from "@mui/material";

import {
    CheckCircleRounded,
    LockOutlined,
    Visibility,
    VisibilityOff,
    WifiRounded,
} from "@mui/icons-material";

import { useAuth } from "../../context/AuthContext";

export default function Login() {

    const navigate = useNavigate();

    const { login } = useAuth();

    const [username, setUsername] = useState("");

    const [password, setPassword] = useState("");

    const [showPassword, setShowPassword] = useState(false);

    const [rememberMe, setRememberMe] = useState(true);

    const [loading, setLoading] = useState(false);

    const [error, setError] = useState("");

    const handleSubmit = async (event) => {

        event.preventDefault();

        setError("");

        setLoading(true);

        try {

            await login(
                username,
                password
            );

            navigate("/dashboard");

        } catch (err) {

            setError(
                err?.response?.data?.detail ??
                "Unable to sign in."
            );

        } finally {

            setLoading(false);

        }

    };

    return (

        <Grid
            container
            sx={{
                minHeight: "100vh",
                bgcolor: "#F8FAFC",
            }}
        >

            {/* Left Branding Panel */}

            <Grid
                size={{ xs: 0, md: 7 }}
                sx={{
                    display: {
                        xs: "none",
                        md: "flex",
                    },
                    flexDirection: "column",
                    justifyContent: "space-between",
                    p: 8,
                    color: "white",
                    background:
                        "linear-gradient(135deg,#2563EB 0%,#1D4ED8 50%,#1E3A8A 100%)",
                    position: "relative",
                    overflow: "hidden",
                }}
            >

                <Box
                    sx={{
                        position: "absolute",
                        width: 500,
                        height: 500,
                        borderRadius: "50%",
                        background: "rgba(255,255,255,.05)",
                        top: -180,
                        right: -120,
                    }}
                />

                <Box
                    sx={{
                        position: "absolute",
                        width: 350,
                        height: 350,
                        borderRadius: "50%",
                        background: "rgba(255,255,255,.05)",
                        bottom: -120,
                        left: -100,
                    }}
                />

                <Stack
                    spacing={4}
                    sx={{
                        position: "relative",
                        zIndex: 2,
                    }}
                >

                    <Box
                        sx={{
                            width: 84,
                            height: 84,
                            borderRadius: "50%",
                            bgcolor: "rgba(255,255,255,.15)",
                            backdropFilter: "blur(12px)",
                            display: "flex",
                            alignItems: "center",
                            justifyContent: "center",
                        }}
                    >

                        <WifiRounded
                            sx={{
                                fontSize: 42,
                            }}
                        />

                    </Box>

                    <Box>

                        <Typography
                            variant="h2"
                            fontWeight={700}
                        >
                            BryanNet
                        </Typography>

                        <Typography
                            variant="h5"
                            sx={{
                                mt: 1,
                                opacity: .9,
                            }}
                        >
                            ISP Management Platform
                        </Typography>

                    </Box>

                    <Typography
                        sx={{
                            maxWidth: 520,
                            fontSize: 20,
                            lineHeight: 1.8,
                            opacity: .92,
                        }}
                    >
                        A modern administration platform for
                        managing customers, internet plans,
                        subscriptions, payments and network
                        infrastructure.
                    </Typography>

                    <Stack spacing={3}>

                        {[
                            "Customer Management",
                            "Subscription Management",
                            "Router Automation",
                            "Payment Verification",
                        ].map((item) => (

                            <Stack
                                key={item}
                                direction="row"
                                spacing={2}
                                alignItems="center"
                            >

                                <CheckCircleRounded />

                                <Typography
                                    fontSize={18}
                                >
                                    {item}
                                </Typography>

                            </Stack>

                        ))}

                    </Stack>

                </Stack>

                <Box
                    sx={{
                        position: "relative",
                        zIndex: 2,
                    }}
                >

                    <Typography
                        fontWeight={600}
                    >
                        BryanNet ISP Platform
                    </Typography>

                    <Typography
                        sx={{
                            opacity: .75,
                            mt: .5,
                        }}
                    >
                        Version 1.0.0
                    </Typography>

                </Box>

            </Grid>

            {/* Login Panel */}

            <Grid
                size={{ xs: 12, md: 5 }}
                sx={{
                    display: "flex",
                    justifyContent: "center",
                    alignItems: "center",
                    p: {
                        xs: 3,
                        md: 6,
                    },
                }}
            >

                <Card
                    elevation={0}
                    sx={{
                        width: "100%",
                        maxWidth: 460,
                        p: 5,
                        borderRadius: 5,
                        border: "1px solid #E2E8F0",
                        boxShadow:
                            "0 25px 60px rgba(15,23,42,.08)",
                    }}
                >

                    <Stack spacing={4}>

                        <Stack
                            spacing={2}
                            alignItems="center"
                        >

                            <Box
                                sx={{
                                    width: 72,
                                    height: 72,
                                    borderRadius: "50%",
                                    bgcolor: "#EFF6FF",
                                    display: "flex",
                                    alignItems: "center",
                                    justifyContent: "center",
                                }}
                            >

                                <LockOutlined
                                    sx={{
                                        fontSize: 36,
                                        color: "#2563EB",
                                    }}
                                />

                            </Box>

                            <Box textAlign="center">

                                <Typography
                                    variant="h4"
                                    fontWeight={700}
                                >
                                    Administrator Sign In
                                </Typography>

                                <Typography
                                    color="text.secondary"
                                >
                                    Sign in to continue to your
                                    administrator dashboard.
                                </Typography>

                            </Box>

                        </Stack>

                        {error && (

                            <Alert severity="error">

                                {error}

                            </Alert>

                        )}

                        <Box
                            component="form"
                            onSubmit={handleSubmit}
                        >

                            <Stack spacing={3}>

                                <TextField
                                    label="Username"
                                    placeholder="Enter your username"
                                    value={username}
                                    onChange={(e) =>
                                        setUsername(
                                            e.target.value
                                        )
                                    }
                                    fullWidth
                                    required
                                    autoFocus
                                    autoComplete="username"
                                />

                                <TextField
                                    label="Password"
                                    placeholder="Enter your password"
                                    type={
                                        showPassword
                                            ? "text"
                                            : "password"
                                    }
                                    value={password}
                                    onChange={(e) =>
                                        setPassword(
                                            e.target.value
                                        )
                                    }
                                    fullWidth
                                    required
                                    autoComplete="current-password"
                                    slotProps={{
                                        input: {
                                            endAdornment: (
                                                <InputAdornment position="end">

                                                    <IconButton
                                                        aria-label="toggle password visibility"
                                                        edge="end"
                                                        onClick={() =>
                                                            setShowPassword(
                                                                (show) => !show
                                                            )
                                                        }
                                                    >

                                                        {showPassword ? (

                                                            <VisibilityOff />

                                                        ) : (

                                                            <Visibility />

                                                        )}

                                                    </IconButton>

                                                </InputAdornment>
                                            ),
                                        },
                                    }}
                                />

                                <FormControlLabel
                                    control={
                                        <Checkbox
                                            checked={rememberMe}
                                            onChange={(e) =>
                                                setRememberMe(
                                                    e.target.checked
                                                )
                                            }
                                        />
                                    }
                                    label="Remember me"
                                />

                                <Button
                                    type="submit"
                                    variant="contained"
                                    size="large"
                                    disabled={loading}
                                    sx={{
                                        height: 54,
                                        borderRadius: 3,
                                        textTransform: "none",
                                        fontSize: 16,
                                        fontWeight: 700,
                                        boxShadow: "none",

                                        "&:hover": {
                                            boxShadow:
                                                "0 12px 28px rgba(37,99,235,.30)",
                                        },
                                    }}
                                >

                                    {loading ? (

                                        <CircularProgress
                                            size={24}
                                            color="inherit"
                                        />

                                    ) : (

                                        "Sign In"

                                    )}

                                </Button>

                            </Stack>

                        </Box>

                        <Box
                            sx={{
                                pt: 3,
                                borderTop: "1px solid",
                                borderColor: "divider",
                            }}
                        >

                            <Typography
                                variant="body2"
                                color="text.secondary"
                                align="center"
                            >
                                Authorized personnel only
                            </Typography>

                            <Typography
                                variant="body2"
                                color="text.secondary"
                                align="center"
                                sx={{
                                    mt: 1,
                                }}
                            >
                                BryanNet ISP Platform © 2026
                            </Typography>

                        </Box>

                    </Stack>

                </Card>

            </Grid>

        </Grid>

    );

}
