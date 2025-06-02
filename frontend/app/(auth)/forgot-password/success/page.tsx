import React from "react";
import Success from "@/app/component/Success/Success";

export default async function ForgotPasswordSuccessfull() {
    const copy = "If this email matches an existing account, you will receive an email with instructions to reset your password."
    return (
      <div>
        <Success copy={copy} />
      </div>
    );
}