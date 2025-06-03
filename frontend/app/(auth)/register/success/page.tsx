"use client";

import React from "react";
import Success from "@/components/Success/Success";

export default function RegistrationSuccessful() {
    const copy = "You have been successfully registered. Please check your email to confirm your registration. \n The confirmation e-mail will direct you to a new login screen.";
    return (
        <div>
            <Success copy={copy} />
        </div>
    );
}