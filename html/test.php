<?php
echo "<h1>Home Lab Test Page</h1>";
echo "<p>Current Time: " . date('Y-m-d H:i:s') . "</p>";
echo "<h2>Server Information:</h2>";
echo "<ul>";
echo "<li>Server IP: " . $_SERVER['SERVER_ADDR'] . "</li>";
echo "<li>PHP Version: " . phpversion() . "</li>";
echo "<li>Document Root: " . $_SERVER['DOCUMENT_ROOT'] . "</li>";
echo "</ul>";

// Test database connection
try {
    $pdo = new PDO('mysql:host=db;dbname=appdb', 'appuser', 'userpass');
    echo "<p style='color:green'>✅ Database Connected Successfully!</p>";
    
    // Create a test table
    $pdo->exec("CREATE TABLE IF NOT EXISTS test_connection (
        id INT AUTO_INCREMENT PRIMARY KEY,
        test_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )");
    echo "<p>✅ Test table created/verified</p>";
    
} catch (PDOException $e) {
    echo "<p style='color:red'>❌ Database Error: " . $e->getMessage() . "</p>";
}
?>
