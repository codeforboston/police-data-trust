import React from "react";
import Success from "@/app/component/Success/Success";

export default async function RegistrationSuccessful() {
    const copy = "You have been successfully registered. \n Please check your email to confirm your registration. \n The confirmation e-mail will direct you to a new login screen.";
    return (
        <div>
            <Success copy={copy} />
        </div>
    );
}