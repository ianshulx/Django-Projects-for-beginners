import java.awt.*;
import java.awt.event.*;
import javax.swing.*;

public class TimerApp {
    static JFrame window = new JFrame("TIMER");
    static JTextField minutes = new JTextField();
    static JTextField seconds = new JTextField();
    private static javax.swing.Timer countdownTimer;
    private static int secondsRemaining;
    private static int minutesRemaining;

    public static void main(String[] args) {
        //frame
        window.getContentPane().setLayout(new BorderLayout());
        window.setSize(600, 450);
        window.getContentPane().setBackground(Color.lightGray);
        window.setLocationRelativeTo(null);
        //buttons
        JButton start = new JButton("Start Timer");
        JButton pause = new JButton("Pause Timer");
        JButton reset = new JButton("Reset Timer");
        customizeButton(start);
        customizeButton(pause);
        customizeButton(reset);
        JPanel buttons = new JPanel(new GridLayout(1, 3));
        buttons.add(start);
        buttons.add(pause);
        buttons.add(reset);
        //input
        JPanel input = new JPanel(new GridLayout(1, 3));
        minutes.setText("00");
        seconds.setText("00");
        minutes.setHorizontalAlignment(JTextField.CENTER);
        seconds.setHorizontalAlignment(JTextField.CENTER);
        minutes.setFont(minutes.getFont().deriveFont(40f));
        seconds.setFont(seconds.getFont().deriveFont(40f));
        input.add(minutes);
        JLabel colon = new JLabel(":", SwingConstants.CENTER);
        colon.setFont(colon.getFont().deriveFont(40f));
        input.add(colon);
        input.add(seconds);

        //center
        JPanel panel = new JPanel(new GridLayout(2, 1));
        panel.add(input);
        panel.add(buttons);

        window.getContentPane().add(panel, BorderLayout.CENTER);
        window.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        window.setVisible(true);

        //button functions
        start.addActionListener(e -> startCountdown());
        pause.addActionListener(e -> {
            if (countdownTimer != null) countdownTimer.stop();
        });
        reset.addActionListener(e -> {
            if (countdownTimer != null) countdownTimer.stop();
            minutes.setText("00");
            seconds.setText("00");
        });
    }

    private static void startCountdown() {
        if (minutes.getText().isEmpty()) minutes.setText("00");
        if (seconds.getText().isEmpty()) seconds.setText("00");

        minutesRemaining = Integer.parseInt(minutes.getText());
        secondsRemaining = Integer.parseInt(seconds.getText());

        if (countdownTimer != null && countdownTimer.isRunning()) {
            countdownTimer.stop();
        }
        countdownTimer = new javax.swing.Timer(1000, new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                if (secondsRemaining == 0) {
                    if (minutesRemaining == 0) {
                        countdownTimer.stop();
                        showTimesUp();
                        return;
                    } else {
                        minutesRemaining--;
                        secondsRemaining = 59;
                    }
                } else {
                    secondsRemaining--;
                }

                minutes.setText(String.format("%02d", minutesRemaining));
                seconds.setText(String.format("%02d", secondsRemaining));
            }
        });
        countdownTimer.start();
    }

    private static void showTimesUp() {
    window.getContentPane().removeAll();
    window.setSize(2000, 1700);
    window.getContentPane().setBackground(Color.black);
    window.setLocationRelativeTo(null);
    //Big "TIME'S UP!" label
    JLabel text = new JLabel("TIME'S UP!", SwingConstants.CENTER);
    text.setForeground(Color.lightGray);
    text.setFont(text.getFont().deriveFont(120.0f));
    //Ensure the window is in front
    window.setAlwaysOnTop(true);
    window.toFront();
    window.requestFocus();


    //Large Clear button
    JButton clear = new JButton("CLEAR");
    clear.setFont(clear.getFont().deriveFont(40.0f));
    clear.setFocusPainted(false); // no ugly focus border
    clear.setPreferredSize(new Dimension(400, 100)); // rectangle shape
    clear.setCursor(Cursor.getPredefinedCursor(Cursor.HAND_CURSOR));
    clear.addActionListener(e -> {
        window.getContentPane().removeAll();
        main(null); // rebuild UI
        window.setAlwaysOnTop(false);
        window.revalidate();
        window.repaint();
    });

    //Panel to hold text + button stacked vertically
    JPanel centerPanel = new JPanel(new BorderLayout());
    centerPanel.setBackground(Color.black);
    centerPanel.add(text, BorderLayout.CENTER);

    JPanel buttonPanel = new JPanel();
    buttonPanel.setBackground(Color.black);
    buttonPanel.add(clear);

    centerPanel.add(buttonPanel, BorderLayout.SOUTH);

    //d to frame
    window.getContentPane().add(centerPanel, BorderLayout.CENTER);

    window.revalidate();
    window.repaint();
}
private static void customizeButton(JButton button) {
    button.setCursor(Cursor.getPredefinedCursor(Cursor.HAND_CURSOR));
    button.setFont(new Font("SansSerif", Font.PLAIN, 16));
}
}
