package com.trancendos.alervato.controller;

import com.trancendos.alervato.dto.TransactionDTO;
import com.trancendos.alervato.model.Transaction;
import com.trancendos.alervato.service.TransactionService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/transactions")
@CrossOrigin(origins = "*")
public class TransactionController {

    @Autowired
    private TransactionService transactionService;

    /**
     * Retrieves a paginated list of transactions for the authenticated user.
     *
     * @param authentication The authentication object containing the user's details.
     * @param pageable The pagination information.
     * @return A `ResponseEntity` containing a page of transactions.
     */
    @GetMapping
    public ResponseEntity<Page<Transaction>> getUserTransactions(
            Authentication authentication,
            Pageable pageable) {
        String username = authentication.getName();
        Page<Transaction> transactions = transactionService.getUserTransactions(username, pageable);
        return ResponseEntity.ok(transactions);
    }

    /**
     * Creates a new transaction for the authenticated user.
     *
     * @param transactionDTO The request body containing the transaction details.
     * @param authentication The authentication object containing the user's details.
     * @return A `ResponseEntity` containing the created transaction, or an error message.
     */
    @PostMapping
    public ResponseEntity<?> createTransaction(
            @Valid @RequestBody TransactionDTO transactionDTO,
            Authentication authentication) {
        try {
            String username = authentication.getName();
            Transaction transaction = transactionService.createTransaction(transactionDTO, username);
            return ResponseEntity.ok(transaction);
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(e.getMessage());
        }
    }

    /**
     * Retrieves a specific transaction by its ID for the authenticated user.
     *
     * @param id The ID of the transaction to retrieve.
     * @param authentication The authentication object containing the user's details.
     * @return A `ResponseEntity` containing the requested transaction, or a not found response.
     */
    @GetMapping("/{id}")
    public ResponseEntity<?> getTransaction(
            @PathVariable Long id,
            Authentication authentication) {
        try {
            String username = authentication.getName();
            Transaction transaction = transactionService.getTransactionById(id, username);
            return ResponseEntity.ok(transaction);
        } catch (Exception e) {
            return ResponseEntity.notFound().build();
        }
    }

    /**
     * Updates an existing transaction for the authenticated user.
     *
     * @param id The ID of the transaction to update.
     * @param transactionDTO The request body containing the updated transaction details.
     * @param authentication The authentication object containing the user's details.
     * @return A `ResponseEntity` containing the updated transaction, or an error message.
     */
    @PutMapping("/{id}")
    public ResponseEntity<?> updateTransaction(
            @PathVariable Long id,
            @Valid @RequestBody TransactionDTO transactionDTO,
            Authentication authentication) {
        try {
            String username = authentication.getName();
            Transaction transaction = transactionService.updateTransaction(id, transactionDTO, username);
            return ResponseEntity.ok(transaction);
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(e.getMessage());
        }
    }

    /**
     * Deletes a transaction for the authenticated user.
     *
     * @param id The ID of the transaction to delete.
     * @param authentication The authentication object containing the user's details.
     * @return A `ResponseEntity` indicating the result of the deletion attempt.
     */
    @DeleteMapping("/{id}")
    public ResponseEntity<?> deleteTransaction(
            @PathVariable Long id,
            Authentication authentication) {
        try {
            String username = authentication.getName();
            transactionService.deleteTransaction(id, username);
            return ResponseEntity.ok().body("Transaction deleted successfully");
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(e.getMessage());
        }
    }
}