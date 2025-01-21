// Copyright (c) 2025 Arista Networks, Inc.
// Use of this source code is governed by the Apache License 2.0
// that can be found in the LICENSE file.

mod sha512crypt;

use pyo3::{
    pyfunction, pymodule,
    types::{PyModule, PyModuleMethods},
    wrap_pyfunction, Bound,
};

#[pyfunction]
/// Computes the SHA512 crypt value for the password given the salt
///
/// The number of rounds is hardcoded to 5000 as expected by EOS.
///
/// Parameters:
///   password: The password.
///   salt: The salt to use (should be 16 in length max or will be truncated).
///
/// Returns:
///   str: The sha512 crypt value.
pub fn sha512_crypt(password: String, salt: String) -> String {
    let result = sha512crypt::main(password, salt);

    match result {
        Ok(res) => res,
        Err(e) => format!("{e:?}").to_string(),
        // Err(e) => serde_json::to_string(&e).unwrap(),
    }
}

#[pymodule]
#[pyo3(name = "_passwords")]
fn passwords(m: &Bound<'_, PyModule>) -> pyo3::PyResult<()> {
    m.add_function(wrap_pyfunction!(sha512_crypt, m)?)?;
    Ok(())
}
